from django.http import JsonResponse
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


class AgencyBranches(generics.ListAPIView):
    serializer_class=BranchDetailsSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,CanCreateBranches]

    def get_queryset(self):
        pk= self.kwargs['pk']
        branches=Branch.objects.filter(agency=pk)
        return branches
    

class AgencyBranchesDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated,IsAgency,CanRudBranches]
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
    permission_classes=[IsAuthenticatedOrReadOnly,IsAgencyOrReadOnly,IsBranchOwner]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['owned_by__wilaya','engine','transmission','type','price','options']
    search_fields = ['make__name','model__name','engine__name','transmission__name','type__name','price','options__name']

    def get_serializer_class(self):
        if self.request.method=='GET':
            return VehicleDetailsSerializer
        elif self.request.method=='POST':
            return VehicleSerializer

    def  get_queryset(self):
        vehicles=Vehicle.objects.filter(is_available=True,is_deleted=False)
        return vehicles
    

    def create(self, request, *args, **kwargs):
        agency=Agency.objects.get(user=request.user)
        branches=Branch.objects.filter(agency=agency)
        branch_pk=request.data.get('owned_by')
    
        try :
            branch=Branch.objects.get(pk=branch_pk)
            print(f'branch: {branch}')
            if branch in branches:
                return super().create(request, *args, **kwargs) 
            else:
                return Response("you can't perfor this action",status=status.HTTP_400_BAD_REQUEST)    
        except Branch.DoesNotExist:
            return Response("branch doesn't exist",status=status.HTTP_404_NOT_FOUND)

class VehicleDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAgencyOrReadOnly,
        IsBranchOwner,
        CanRudVehicles
    ]
    queryset = Vehicle.objects.all()
    def get_serializer_class(self):
        if self.request.method=='GET':
            return VehicleDetailsSerializer
        else:
            return VehicleSerializer

    def delete(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.is_deleted=True
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
    permission_classes=[permissions.IsAuthenticated,IsAgency]

    def get_queryset(self):
        user=self.request.user
        agency=Agency.objects.get(user=user)
        resrvations=Reservation.objects.filter(agency=agency)
        return resrvations
    
# display and edit a specific reservation (accept or decline)
class ReservationDetails(generics.RetrieveAPIView):
    serializer_class=AgencyReservationDetailsSerializer
    permission_classes=[permissions.IsAuthenticated,IsAgency,CanRudReservation]
    queryset=Reservation.objects.all()



class AcceptReservation(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = AgencyReservationDetailsSerializer
    permission_classes=[permissions.IsAuthenticated,IsAgency,CanRudReservation]

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
    permission_classes=[permissions.IsAuthenticated,IsAgency,CanRudReservation]


    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Mark the reservation as accepted
        instance.status='refused'
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    




@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAgency])
def agencyOverview(request):
    user=request.user
    agency=Agency.objects.get(user=user)
    serializer=OverviewAgencySerializer(agency)
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