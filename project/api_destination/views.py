from django.shortcuts import render
from rest_framework import generics
from api_destination.models import *
from api_destination.serializers import *
from api_destination.permissions import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api_main.permissions import IsDefaultOrReadOly
# Create your views here.

# class ListCreateDestinationCategory(generics.ListCreateAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.all()
#     permission_classes = []


class ListCreateDestination(generics.ListCreateAPIView):
    serializer_class = DestinationSerializer
    queryset = Destination.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,IsDefaultOrReadOly]


class DestinationDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DestinationSerializer
    queryset = Destination.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,IsDefaultOrReadOly,IsDestinationOwner]
