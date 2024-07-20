from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from api_auth.models import User
from api_auth.serializers import UserDetailsSerializer
from api_agency.serializers import AgencyDetailSerializer,AgencySerializer,RateDetailsSerializer,BranchDetailsSerializer,VehicleDetailsSerializer,VehicleSerializer,AgencyReservationDetailsSerializer,FeedbackSerializer
from api_agency.models import Agency,Branch,Vehicle,Reservation,Rate,Feedback
from api_admin.permissions import IsAdmin
from api_admin.serializers import *
from api_destination.models import Destination,DestinationRate,DestinationFeedback
# from api_destination.serializers import DestinationSerializer,RateDetailsSerializer
import api_destination.serializers as api_destination_serializers
from api_activity.models import Activity,ActivityRate,ActivityFeedback
import api_activity.serializers as api_acticity_serializers
# Create your views here.



class AdminUserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAdmin]

class AdminUserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailsSerializer
        else:
            return AdminUserUpdateSerializer
    


class AdminAgencyList(generics.ListAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencyDetailSerializer
    permission_classes = [IsAdmin]

class AdminValidateAgency(generics.UpdateAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencyDetailSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_validated != True:
            print(F"Agency not validated")
            instance.is_validated = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminAgencyDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agency.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AgencyDetailSerializer
        else:
            return AgencySerializer


class AdminAgencyRatings(generics.ListAPIView):
    queryset = Rate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = RateDetailsSerializer


class AdminAgencyRatingsDetails(generics.RetrieveDestroyAPIView):
    queryset = Rate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = RateDetailsSerializer


class AdminAgencyFeedbacks(generics.ListAPIView):
    queryset = Feedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = FeedbackSerializer


class AdminAgencyFeedbacksDetails(generics.RetrieveDestroyAPIView):
    queryset = Feedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = FeedbackSerializer



class AdminBranchList(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminBranchSerializer
        else:
            return BranchDetailsSerializer
        


class AdminBranchDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BranchDetailsSerializer
        else:
            return AdminBranchSerializer
        



class AdminVehicleList(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = VehicleDetailsSerializer


class AdminVehicleDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    permission_classes = [IsAdmin]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return VehicleDetailsSerializer
        else:
            return VehicleSerializer
        

class AdminReservationList(generics.ListAPIView):
    queryset = Reservation.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = AgencyReservationDetailsSerializer




class AdminReservationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AgencyReservationDetailsSerializer
        else:
            return AdminReservationSerializer
        

class AdminDestinationList(generics.ListAPIView):
    queryset = Destination.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = AdminDestinationSerializer

class AdminDestinationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AdminDestinationSerializer
        else:
            return api_destination_serializers.DestinationSerializer


class AdminDestinationRatings(generics.ListAPIView):
    queryset = DestinationRate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_destination_serializers.RateDetailsSerializer



class AdminDestinationRatingsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = DestinationRate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_destination_serializers.RateDetailsSerializer

class AdminDestinationFeedbacks(generics.ListAPIView):
    queryset = DestinationFeedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_destination_serializers.FeedbackSerializer


class AdminDestinationFeedbacksDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = DestinationFeedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_destination_serializers.FeedbackSerializer



class AdminActivityList(generics.ListAPIView):
    queryset = Activity.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = AdminActivitySerializer



class AdminActivityDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AdminActivitySerializer
        else:
            return api_acticity_serializers.ActivitySerializer
        

class AdminActivityRatings(generics.ListAPIView):
    queryset = ActivityRate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_acticity_serializers.RateDetailsSerializer


class AdminActivityRatingsDetails(generics.RetrieveDestroyAPIView):
    queryset = ActivityRate.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_acticity_serializers.RateDetailsSerializer



class AdminActivityFeedbacks(generics.ListAPIView):
    queryset = ActivityFeedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_acticity_serializers.FeedbackSerializer



class AdminActivityFeedbacksDetails(generics.RetrieveDestroyAPIView):
    queryset = ActivityFeedback.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = api_acticity_serializers.FeedbackSerializer