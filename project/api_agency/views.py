
from rest_framework.decorators import api_view,permission_classes
from api_agency.serializers import *
from rest_framework.response import Response
from rest_framework import status
from api_agency.permissions import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework import generics
from rest_framework.authtoken.views import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api_main.permissions import IsDefault
from api_agency.filters import VehcilePriceFilter


# Create your views here.


#--------------Agencies-------------#

class Agencies(generics.ListCreateAPIView):

    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [permissions.AllowAny]




class AgencyDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencyDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAgencyOwnerOrReadOnly]


@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAgency])
def agencyProfile(request):
    user=request.user
    agency=Agency.objects.get(user=user)
    serializer=AgencySerializer(agency)
    return Response(serializer.data,status=status.HTTP_200_OK)


#------------------Branches-------------#

class Branches(generics.ListCreateAPIView):
    queryset=Branch.objects.all()
    serializer_class=BranchSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,IsAgencyOrReadOnly]

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return BranchDetailsSerializer
        elif self.request.method == 'POST':
            return BranchSerializer


class BranchDetails(generics.RetrieveAPIView):
    queryset=Branch.objects.all()
    serializer_class=BranchDetailsSerializer
    permission_classes=[permissions.AllowAny]


class BranchVehicles(generics.ListAPIView):
    serializer_class=VehicleDetailsSerializer
    permission_classes=[permissions.AllowAny]
    def get_queryset(self):
        pk= self.kwargs['pk']
        vehicles=Vehicle.objects.filter(owned_by=pk,is_deleted=False)
        return vehicles

class AgencyBranches(generics.ListAPIView):
    serializer_class=BranchDetailsSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,CanCreateBranches]

    def get_queryset(self):
        pk= self.kwargs['pk']
        branches=Branch.objects.filter(agency=pk)
        return branches
    


class AgencyBranchesDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated,CanRudBranches]
    queryset=Branch.objects.all()
    
    def get_serializer_class(self):

        if self.request.method == 'GET':
            return BranchDetailsSerializer
        else:
            return BranchSerializer





#----------------------------VEHICLES-------------------#
#LIST vehicles and models 
@api_view(['GET'])
def vehicles_makes(request):
    makes=Make.objects.all()
    serializer=MakeSerializer(makes,many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def vehicles_models(request,pk):
    models=Model.objects.filter(make_id=pk)
    serializer=ModelSerializer(models,many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)


#VEHICLES MANAGEMENT FOR AGENCIES


class ListVehicles(generics.ListCreateAPIView):
    # serializer_class=VehicleSerializer
    # permission_classes=[IsAuthenticatedOrReadOnly,IsAgencyOrReadOnly,IsBranchOwner]
    permission_classes=[IsAuthenticatedOrReadOnly,CanRudVehicles]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['owned_by__wilaya','engine','transmission','type','options']
    filterset_class = VehcilePriceFilter
    search_fields = ['make__name','model__name','engine__name','transmission__name','type__name','options__name']
    def get_serializer_class(self):
        if self.request.method=='GET':
            return VehicleDetailsSerializer
        elif self.request.method=='POST':
            return VehicleSerializer

    def  get_queryset(self):
        vehicles=Vehicle.objects.filter(is_available=True,is_deleted=False)
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price :
            vehicles = vehicles.filter(price__gte=min_price)
        if max_price :
            vehicles = vehicles.filter(price__lte=max_price)
        return vehicles
    

    # def create(self, request, *args, **kwargs):
    #     agency=Agency.objects.get(user=request.user)
    #     branches=Branch.objects.filter(agency=agency)
    #     branch_pk=request.data.get('owned_by')
    #     # search if the given branch is actually linked to the conneted agency
    #     try :
    #         branch=Branch.objects.get(pk=branch_pk)
    #         if branch in branches:
    #             # if True permission granted to create vehicle and assign it to the branch
    #             return super().create(request, *args, **kwargs) 
    #         else:
    #             return Response("you can't perfor this action",status=status.HTTP_400_BAD_REQUEST)    
    #     except Branch.DoesNotExist:
    #         return Response("branch doesn't exist",status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        #check if the user is branch or agency

        if request.user.role == 'branch_admin':
            branch = Branch.objects.get(user = request.user)
            request.data['owned_by']=branch.pk
            print(request.data)
        elif request.user.role == 'agency_admin':
            agency = Agency.objects.get(user=request.user)
            try :
                branch_pk = request.data['owned_by']
                branch = Branch.objects.get(pk=branch_pk)
                if branch.agency == agency:
                    request.data['owned_by']=branch.pk
                else:
                    raise Branch.DoesNotExist
            except Branch.DoesNotExist:
                return Response("branch doesn't exist",status=status.HTTP_404_NOT_FOUND)
        return super().create(request, *args, **kwargs)


class VehicleDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        # IsAgencyOrReadOnly,
        # IsBranchOwner,
        CanRudVehicles
    ]
    queryset = Vehicle.objects.all()
    def get_serializer_class(self):
        if self.request.method=='GET':
            return VehicleDetailsSerializer
        else:
            return VehicleSerializer


    def update(self, request, *args, **kwargs):
        if request.user.role == 'branch_admin':
                branch = Branch.objects.get(user = request.user)
                pass 
        elif request.user.role == 'agency_admin':
            agency = Agency.objects.get(user=request.user)
            try :
                branch_pk = request.data['owned_by']
                branch = Branch.objects.get(pk=branch_pk)
                if branch.agency == agency:
                    request.data['owned_by']=branch.pk
                else:
                    raise Branch.DoesNotExist
            except Branch.DoesNotExist:
                return Response("branch doesn't exist",status=status.HTTP_404_NOT_FOUND)
        return super().update(request, *args, **kwargs)
        
    def delete(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.is_deleted=True
        instance.is_available=False
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class VehicleImageDelete(generics.DestroyAPIView):
    queryset=VehicleImage.objects.all()
    serializer_class=VehicleImageSerializer
    permission_classes=[IsAuthenticated,IsAgency,CanDestroyVehicleImage]
    


class AgencyVehicles(generics.ListAPIView):
    serializer_class=VehicleDetailsSerializer
    permission_classes=[permissions.AllowAny]
    queryset=Vehicle.objects.all()
    def get_queryset(self):
        pk= self.kwargs['pk']
        vehicles=Vehicle.objects.filter(owned_by__agency=pk,is_deleted=False)
        return vehicles
        
#list the reservation of the logged  agency
class ReservationList(generics.ListAPIView):
    serializer_class=AgencyReservationDetailsSerializer
    permission_classes=[permissions.IsAuthenticated,CanRudReservation]

    def get_queryset(self):
        user=self.request.user
        if user.role == 'agency_admin':
            agency=Agency.objects.get(user=user)
            branch_pk = self.request.GET.get('branch_pk') # we can send it in the request body
            resrvations=Reservation.objects.filter(branch__agency=agency)
            if branch_pk:#if branch_pk is sent by the agency we can filter reservation by branch id 
                try:
                    branch=Branch.objects.get(pk=branch_pk)
                    if branch.agency != agency:
                        raise ValidationError("You don't have permission")
                except Branch.DoesNotExist:
                    raise ValidationError("Branch with ID {} does not exist".format(branch_pk))
                resrvations = resrvations.filter(branch = branch_pk)
        elif user.role == 'branch_admin':
            branch = Branch.objects.get(user = user)
            resrvations = Reservation.objects.filter(branch = branch)
        return resrvations
    
# display and edit a specific reservation (accept or decline)
class ReservationDetails(generics.RetrieveAPIView):
    serializer_class=AgencyReservationDetailsSerializer
    permission_classes=[permissions.IsAuthenticated,CanRudReservation]
    queryset=Reservation.objects.all()


class AcceptReservation(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = AgencyReservationDetailsSerializer
    permission_classes=[permissions.IsAuthenticated,CanRudReservation]

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
    serializer_class = AgencyReservationDetailsSerializer
    permission_classes=[permissions.IsAuthenticated,CanRudReservation]


    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Mark the reservation as refused
        instance.status='refused'
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Agency Rate

class RateAgency(generics.CreateAPIView):
    serializer_class = RateSerializer
    queryset = Rate.objects.all()
    permission_classes= [permissions.IsAuthenticated,IsDefault,]
    

class AgencyRatings(generics.ListAPIView):
    serializer_class = RateDetailsSerializer

    def get_queryset(self):
        try :
            agency_pk=self.kwargs["pk"]
            agency=Agency.objects.get(pk=agency_pk)
            ratings=Rate.objects.filter(agency=agency)
            return ratings
        except Agency.DoesNotExist:
            raise ValidationError("Agency with ID {} does not exist".format(agency_pk))

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAgency])
def agencyOverview(request):
    user=request.user
    agency=Agency.objects.get(user=user)
    serializer=OverviewAgencySerializer(agency)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsBranchOwner])
def branchOverview(request):
    user=request.user
    branch=Branch.objects.get(user=user)
    serializer=OverviewBranchSerializer(branch)
    return Response(serializer.data,status=status.HTTP_200_OK)



@api_view(['GET'])
def get_details(request):
    data={
    'types':TypeSerializer(Type.objects.all(),many=True).data,
    'energies':EnergySerializer(Energy.objects.all(),many=True).data,
    'transmissions':TransmissionSerializer(Transmission.objects.all(),many=True).data,
    'options':OptionSerializer(Option.objects.all(),many=True).data
    }

    return Response(data=data,status=status.HTTP_200_OK)


@api_view(['GET'])
def get_wilayas(request):
    wilayas=Wilaya.objects.all()
    serializer=WilayaSerializer(wilayas,many=True)
    return Response(data=serializer.data,status=status.HTTP_200_OK)