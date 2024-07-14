from django.shortcuts import render
from rest_framework import generics
from api_activity.serializers import *
from api_activity.models import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from api_main.permissions import IsDefaultOrReadOly,IsDefault
from api_activity.permissions import *
# Create your views here.

class ListCtreateActivity(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,IsDefaultOrReadOly]


class ActivityDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,IsDefaultOrReadOly,IsActivityOwner]


class RateActivity(generics.CreateAPIView):
    serializer_class = RateSerializer
    queryset = ActivityRate.objects.all()
    permission_classes = [IsAuthenticated,IsDefault]

class ActivityRatings(generics.ListAPIView):
    serializer_class = RateDetailsSerializer

    def get_queryset(self):
        try :
            activity_pk=self.kwargs["pk"]
            activity=Activity.objects.get(pk=activity_pk)
            ratings=ActivityRate.objects.filter(activity=activity)
            return ratings
        except Activity.DoesNotExist:
            raise serializers.ValidationError("Activity with ID {} does not exist".format(activity_pk))



class FeedbackListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,IsDefaultOrReadOly]


    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateFeedbackSerializer
        else:
            return FeedbackSerializer
        
    def get_queryset(self):
        try :
            activity_pk=self.kwargs["pk"]
            activity=Activity.objects.get(pk=activity_pk)
            feedbacks=ActivityFeedback.objects.filter(activity=activity)
            return feedbacks
        except Activity.DoesNotExist:
            raise serializers.ValidationError("Activity with ID {} does not exist".format(activity_pk))
        



class FeedbackDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = ActivityFeedback.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,IsDefaultOrReadOly,CanEditRateFeedback]
    
    def get_serializer_class(self):
        if self.request.method in ["PUT","PATCH"] :
            return CreateFeedbackSerializer
        else:
            return FeedbackSerializer
    