from rest_framework import generics
from api_main.serializers import *
from api_main.models import *
from rest_framework import permissions
from api_main.permissions import *


# Create your views here.

class ProfileList(generics.ListCreateAPIView):
    queryset=Profile.objects.all()
    permission_classes=[permissions.AllowAny]


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileDetailsSerializer
        elif self.request.method == 'POST':
            return ProfileSerializer


class ProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ProfileDetailsSerializer
    queryset=Profile.objects.all()
    permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsProfileOwner]

#list or create reservatoin for the logged in client
class MyReservations(generics.ListCreateAPIView):
    permission_classes=[permissions.IsAuthenticated,IsDefault]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientReservationDetailsSerializer
        elif self.request.method == 'POST':
            return ReservationSerializer

    def get_queryset(self):
        user=self.request.user
        reservations=Reservation.objects.filter(client__user=user)
        return reservations

    def perform_create(self, serializer):
        #get the logged client
        client = Profile.objects.get(user = self.request.user)
        serializer_data=serializer.validated_data
        vehicle = serializer_data.get('vehicle')
        branch = vehicle.owned_by
        start_date = serializer_data['start_date']
        end_date = serializer_data['end_date']
        total_days = (end_date-start_date).days
        total_price = total_days * vehicle.price
        # add calculated data to the serializer validated data
        serializer.validated_data['total_days']=total_days
        serializer.validated_data['total_price']=total_price
        serializer.validated_data['client']=client
        serializer.validated_data['branch']=branch
        return super().perform_create(serializer)
# Display and edit (change date or vehicle or delete) a specific reservation for the logged in client if the reservation is postponed
class Myreservation(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= ClientReservationDetailsSerializer
    queryset=Reservation.objects.all()
    permission_classes=[permissions.IsAuthenticated,IsDefault,CanEditResrvation,CandDeleteReservation]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientReservationDetailsSerializer
        else:
            return EditReservationSerializer
        

    def perform_update(self, serializer):
        vehicle_price=self.get_object().vehicle.price
        serializer_data=serializer.validated_data
        start_date = serializer_data['start_date']
        end_date = serializer_data['end_date']
        total_days = (end_date-start_date).days
        total_price = total_days * vehicle_price
        # add calculated data to the serializer validated data
        serializer.validated_data['total_days']=total_days
        serializer.validated_data['total_price']=total_price
        return super().perform_update(serializer)
    

