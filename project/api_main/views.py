from django.shortcuts import render
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
    

# view and edit (change date or vehicle or delete) a specific reservation for the logged in client if the reservation is postponed
class Myreservation(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= ClientReservationDetailsSerializer
    queryset=Reservation.objects.all()
    permission_classes=[permissions.IsAuthenticated,IsDefault,CanEditResrvation,CandDeleteReservation]
    