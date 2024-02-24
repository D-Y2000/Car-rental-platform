from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from api_agency.serializers import *
from api_agency.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
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



class BranchDetails(generics.RetrieveAPIView):
    queryset=Branch.objects.all()
    serializer_class=BranchSerializer
    permission_classes=[permissions.AllowAny]


class AgencyBranches(generics.ListAPIView):
    serializer_class=BranchSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,CanCreateBranches]

    def get_queryset(self):
        pk= self.kwargs['pk']
        branches=Branch.objects.filter(agency=pk)
        return branches
    

class AgencyBranchesDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=BranchSerializer
    permission_classes=[IsAuthenticated,IsAgency,CanRudBranches]
    queryset=Branch.objects.all()






@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logOut(request):
    token = Token.objects.get(key=request.auth)
    user=token.user
    if user:
        token.delete()
        return Response({'info':'Succefully logged Out!'},status=status.HTTP_200_OK)
    else:
        return Response('Expired Token',status=status.HTTP_400_BAD_REQUEST)
    


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
    queryset=Vehicle.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['owned_by','make','model','current_location','engine','transmission','type','price','options']
    search_fields = ['make__name','model__name','engine__name','transmission__name','type__name','price','options__name']

    def get_serializer_class(self):
        if self.request.method=='GET':
            return VehicleDetailsSerializer
        elif self.request.method=='POST':
            return VehicleSerializer



class VehicleDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticatedOrReadOnly,IsAgencyOrReadOnly,IsBranchOwner,CanRudVehicles]
    queryset=Vehicle.objects.all()
    def get_serializer_class(self):
        if self.request.method=='GET':
            return VehicleDetailsSerializer
        elif self.request.method=='PUT':
            return VehicleSerializer



class AgencyVehicles(generics.ListAPIView):
    serializer_class=VehicleDetailsSerializer
    permission_classes=[permissions.AllowAny]
    queryset=Vehicle.objects.all()
    def get_queryset(self):
        pk= self.kwargs['pk']
        vehicles=Vehicle.objects.filter(owned_by__agency=pk)
        return vehicles
        