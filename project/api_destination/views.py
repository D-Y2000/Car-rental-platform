from django.shortcuts import render
from rest_framework import generics
from api_destination.models import *
from api_destination.serializers import *
from api_destination.permissions import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api_main.permissions import IsDefaultOrReadOly,IsDefault
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

# class ListCreateDestinationCategory(generics.ListCreateAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.all()
#     permission_classes = []


class ListCreateDestination(generics.ListCreateAPIView):
    serializer_class = DestinationSerializer
    queryset = Destination.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,IsDefaultOrReadOly]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['wilaya']
    search_fields = ['name','wilaya__name','address']

class DestinationDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DestinationSerializer
    queryset = Destination.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,IsDefaultOrReadOly,IsDestinationOwner]



class RateDestination(generics.CreateAPIView):
    serializer_class = RateSerializer
    queryset = Rate.objects.all()
    permission_classes= [permissions.IsAuthenticated,IsDefault,]

class DestinationsRatings(generics.ListAPIView):
    serializer_class = RateDetailsSerializer

    def get_queryset(self):
        try :
            destination_pk=self.kwargs["pk"]
            destination=Destination.objects.get(pk=destination_pk)
            ratings=Rate.objects.filter(destination=destination)
            return ratings
        except Destination.DoesNotExist:
            raise serializers.ValidationError("Destination with ID {} does not exist".format(destination_pk))
