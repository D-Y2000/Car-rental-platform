
from rest_framework.decorators import api_view,permission_classes
from api_agency import serializers
from rest_framework.response import Response
from rest_framework import status
from api_agency import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api_main.permissions import IsDefault
from api_agency.filters import VehcilePriceFilter
from django.db.models import F
from api_agency.models import Agency, Branch, Vehicle, VehicleImage, Reservation, Rate, Subscription, Make, Model, Type, Energy, Transmission, Option, Wilaya, Plan 
from django.utils import timezone


# Create your views here.


#--------------Agencies-------------#

class Agencies(generics.ListCreateAPIView):

    queryset = Agency.objects.all()
    serializer_class = serializers.AgencySerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AgencySerializer
        else:
            return serializers.AgencyDetailSerializer
            

class AgencyDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agency.objects.all()
    serializer_class = serializers.AgencyDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,permissions.IsAgencyOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        agency = self.get_object()
        print(f"Retrieved agency: {agency.id}")

        # Check the agency's subscription
        subscription = Subscription.objects.filter(agency=agency).first()
        if subscription and subscription.end_at < timezone.now():
            #unsubscribe agency
            print("Subscription has expired, processing unsubscription")
            self.handle_unsubscription(agency=agency)

        serializer = self.get_serializer(agency)
        return Response(serializer.data)

    def handle_unsubscription(self, agency):
        print(f" starting unsebscription")
        agency_branches = Branch.objects.filter(agency=agency)
        free_plan = Plan.objects.get(name='free')
        unlocked_agency_branches=Branch.objects.filter(agency=agency)[:free_plan.max_branches]
        print(free_plan)
        if agency_branches.count() >= free_plan.max_branches:
            branches_to_lock = Branch.objects.filter(agency=agency)[free_plan.max_branches:]
            #lock all branches and vehicles relaetd to the branches to lock
            print("locking branches")
            for branch in branches_to_lock:
                branch_vehicles = Vehicle.objects.filter(owned_by = branch)
                print("locking branch  vehicles")
                for vehicle in branch_vehicles:
                    vehicle.is_locked = True
                    vehicle.is_available = False
                    vehicle.save()
                print("locking branch")
                branch.is_locked = True
                branch.save()
        #lock vehicles of unlocked branches
        print("unlocked branches")
        for branch in unlocked_agency_branches:
            branch_vehicles = Vehicle.objects.filter(owned_by = branch)
            if branch_vehicles.count() > free_plan.max_vehicles:
                branch_vehicles_to_lock = branch_vehicles[free_plan.max_vehicles:]
                print("locking unlocked branch  vehicles")
                for vehicle in branch_vehicles_to_lock:
                    vehicle.is_locked = True
                    vehicle.is_available = False
                    vehicle.save()
            branch.is_locked = True
            branch.save()


@api_view(['GET'])
@permission_classes([IsAuthenticated,permissions.IsAgency])
def agencyProfile(request):
    user=request.user
    agency=Agency.objects.get(user=user)
    serializer=serializers.AgencySerializer(agency)
    return Response(serializer.data,status=status.HTTP_200_OK)

class AgencySubscription(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated,permissions.IsAgency]

 
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.SubscriptionCreateSerializer
        else:
            return serializers.SubscriptionSerializer
        
    def perform_create(self, serializer):
        user = self.request.user
        agency = Agency.objects.get(user=user)
        serializer.validated_data['agency'] = agency
        return super().perform_create(serializer)
    


#------------------Branches-------------#

class Branches(generics.ListCreateAPIView):
    queryset=Branch.objects.all()
    serializer_class=serializers.BranchSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,permissions.IsAgencyOrReadOnly]

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return serializers.BranchDetailsSerializer
        elif self.request.method == 'POST':
            return serializers.BranchSerializer


class BranchDetails(generics.RetrieveAPIView):
    queryset=Branch.objects.all()
    serializer_class=serializers.BranchDetailsSerializer
    permission_classes=[AllowAny]


class BranchVehicles(generics.ListAPIView):
    serializer_class=serializers.VehicleDetailsSerializer
    permission_classes=[AllowAny]
    def get_queryset(self):
        pk= self.kwargs['pk']
        vehicles=Vehicle.objects.filter(owned_by=pk,is_deleted=False)
        return vehicles

class AgencyBranches(generics.ListAPIView):
    serializer_class=serializers.BranchDetailsSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,permissions.CanCreateBranches]

    def get_queryset(self):
        pk= self.kwargs['pk']
        branches=Branch.objects.filter(agency=pk)
        return branches
    

class AgencyBranchesDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated,permissions.IsAgency,permissions.CanRudBranches]
    queryset=Branch.objects.all()
    
    def get_serializer_class(self):

        if self.request.method == 'GET':
            return serializers.BranchDetailsSerializer
        else:
            return serializers.BranchSerializer





#----------------------------VEHICLES-------------------#
#LIST vehicles and models 
@api_view(['GET'])
def vehicles_makes(request):
    makes=Make.objects.all()
    serializer=serializers.MakeSerializer(makes,many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def vehicles_models(request,pk):
    models=Model.objects.filter(make_id=pk)
    serializer=serializers.ModelSerializer(models,many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)


#VEHICLES MANAGEMENT FOR AGENCIES


class ListVehicles(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticatedOrReadOnly,permissions.IsAgencyOrReadOnly,permissions.IsBranchOwner]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['owned_by__wilaya','engine','transmission','type','options']
    filterset_class = VehcilePriceFilter
    search_fields = ['make__name','model__name','engine__name','transmission__name','type__name','options__name']
    def get_serializer_class(self):
        if self.request.method=='GET':
            return serializers.VehicleDetailsSerializer
        elif self.request.method=='POST':
            return serializers.VehicleSerializer

    def  get_queryset(self):
        vehicles=Vehicle.objects.filter(is_available=True,is_deleted=False)
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price :
            vehicles = vehicles.filter(price__gte=min_price)
        if max_price :
            vehicles = vehicles.filter(price__lte=max_price)
        return vehicles
    

    # increment the clicks_count of the wilaya each time you list vehicles in a certain wilaya
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        wilaya_id = request.GET.get('owned_by__wilaya')
        if wilaya_id:
            Wilaya.objects.filter(id=wilaya_id).update(clicks_count=F('clicks_count')+1)
        return res

    def create(self, request, *args, **kwargs):
        print("create vehicle...")
        img = request.data.get('uploaded_images')
        for i in img:
            print("img", i.get('url'), i.get('order'))
        agency=Agency.objects.get(user=request.user)
        branches=Branch.objects.filter(agency=agency)
        branch_pk=request.data.get('owned_by')
        # search if the given branch is actually linked to the conneted agency
        try :
            branch=Branch.objects.get(pk=branch_pk)
            if branch in branches:
                # if True permission granted to create vehicle and assign it to the branch
                return super().create(request, *args, **kwargs) 
            else:
                return Response("you can't perfor this action",status=status.HTTP_400_BAD_REQUEST)    
        except Branch.DoesNotExist:
            return Response("branch doesn't exist",status=status.HTTP_404_NOT_FOUND)

class VehicleDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        permissions.IsAgencyOrReadOnly,
        permissions.IsBranchOwner,
        permissions.CanRudVehicles
    ]
    queryset = Vehicle.objects.all()
    def get_serializer_class(self):
        if self.request.method=='GET':
            return serializers.VehicleDetailsSerializer
        else:
            return serializers.VehicleSerializer


    def update(self, request, *args, **kwargs):
        agency=Agency.objects.get(user=request.user)
        branches=Branch.objects.filter(agency=agency)
        branch_pk=request.data.get('owned_by')
    
        try :
            branch=Branch.objects.get(pk=branch_pk)
            print(f'branch: {branch}')
            if branch in branches:
                return super().update(request, *args, **kwargs)
            else:
                return Response("you can't perform this action",status=status.HTTP_400_BAD_REQUEST)    
        except Branch.DoesNotExist:
            return Response("branch doesn't exist",status=status.HTTP_404_NOT_FOUND)

        
    def delete(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.is_deleted=True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class VehicleImageDelete(generics.DestroyAPIView):
    queryset=VehicleImage.objects.all()
    serializer_class=serializers.VehicleImageSerializer
    permission_classes=[IsAuthenticated,permissions.IsAgency,permissions.CanDestroyVehicleImage]
    


class AgencyVehicles(generics.ListAPIView):
    serializer_class=serializers.VehicleDetailsSerializer
    permission_classes=[AllowAny]
    queryset=Vehicle.objects.all()
    def get_queryset(self):
        pk= self.kwargs['pk']
        vehicles=Vehicle.objects.filter(owned_by__agency=pk,is_deleted=False,is_locked=False)
        return vehicles
        
#list the reservation of the logged  agency
class ReservationList(generics.ListAPIView):
    serializer_class=serializers.AgencyReservationDetailsSerializer
    permission_classes=[IsAuthenticated,permissions.IsAgency]
    
    def get_queryset(self):
        user=self.request.user
        agency=Agency.objects.get(user=user)
        branch_pk = self.request.GET.get('branch_pk')
        reservations = Reservation.objects.filter(branch__agency=agency)
        if branch_pk :
            reservations= reservations.filter(branch=branch_pk)
        return reservations
    
# display and edit a specific reservation (accept or decline)
class ReservationDetails(generics.RetrieveAPIView):
    serializer_class=serializers.AgencyReservationDetailsSerializer
    permission_classes=[IsAuthenticated,permissions.IsAgency,permissions.CanRudReservation]
    queryset=Reservation.objects.all()



class AcceptReservation(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = serializers.AgencyReservationDetailsSerializer
    permission_classes=[IsAuthenticated,permissions.IsAgency,permissions.CanRudReservation]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Mark the reservation as accepted
        instance.status='accepted'

        # Mark the related vehicle as unavailable
        vehicle = instance.vehicle
        vehicle.is_available = False
        vehicle.save()

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RefuseReservation(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = serializers.AgencyReservationDetailsSerializer
    permission_classes=[IsAuthenticated,permissions.IsAgency,permissions.CanRudReservation]


    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Mark the reservation as accepted
        instance.status='refused'
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Agency Rate

class RateAgency(generics.CreateAPIView):
    serializer_class = serializers.RateSerializer
    queryset = Rate.objects.all()
    permission_classes= [IsAuthenticated,IsDefault,]


class AgencyRatings(generics.ListAPIView):
    serializer_class = serializers.RateDetailsSerializer

    def get_queryset(self):
        try :
            agency_pk=self.kwargs["pk"]
            agency=Agency.objects.get(pk=agency_pk)
            ratings=Rate.objects.filter(agency=agency)
            return ratings
        except Agency.DoesNotExist:
            raise serializers.ValidationError("Agency with ID {} does not exist".format(agency_pk))

@api_view(['GET'])
@permission_classes([IsAuthenticated,permissions.IsAgency])
def agencyOverview(request):
    user=request.user
    agency=Agency.objects.get(user=user)
    serializer=serializers.OverviewAgencySerializer(agency)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated,permissions.IsAgency])
def branchOverview(request,pk):
    user=request.user
    agency=Agency.objects.get(user=user)
    try:
        branch=Branch.objects.get(agency=agency,pk=pk)
        serializer = serializers.OverviewBranchSerializer(branch)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Branch.DoesNotExist:
        raise serializers.ValidationError("Branch with ID {} does not exist".format(pk))


@api_view(['GET'])
def get_details(request):
    data={
    'types': serializers.TypeSerializer(Type.objects.all(),many=True).data,
    'energies': serializers.EnergySerializer(Energy.objects.all(),many=True).data,
    'transmissions': serializers.TransmissionSerializer(Transmission.objects.all(),many=True).data,
    'options': serializers.OptionSerializer(Option.objects.all(),many=True).data
    }

    return Response(data=data,status=status.HTTP_200_OK)


@api_view(['GET'])
def get_wilayas(request):
    wilayas=Wilaya.objects.all()
    serializer=serializers.WilayaSerializer(wilayas,many=True)
    return Response(data=serializer.data,status=status.HTTP_200_OK)

# Get available plans
@api_view(['GET'])
def get_plans(request):
    plan = Plan.objects.all()
    serializer = serializers.PlanSerializer(plan, many=True)
    return Response(data = serializer.data, status = status.HTTP_200_OK)