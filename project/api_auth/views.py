from django.shortcuts import render
from api_auth.models import User
from api_auth.permissions import CanReadNotification
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api_auth.serializers import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework import generics
# Create your views here.
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def UserProfile(request):
#     user=request.user
#     user=User.objects.get(email=user.email)
#     serializer=UserDetailsSerializer(user)
#     return Response(serializer.data,status=status.HTTP_200_OK)

from api_agency.models import Notification
from api_agency.serializers import NotifcationSerializer



class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailsSerializer
        else:
            return UserUpdateSerializer

    def get_object(self):
        user =self.request.user
        return user

class UserListNotifications(generics.ListAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = NotifcationSerializer
    def get_queryset(self):
        user = self.request.user
        notifications = Notification.objects.filter(user=user)
        return notifications
    
class UserNotificationDetails(generics.RetrieveAPIView):
    permission_classes= [IsAuthenticated,CanReadNotification]
    queryset = Notification.objects.all()
    serializer_class = NotifcationSerializer
    def get_object(self):
        instance = super().get_object()
        instance.is_read = True
        instance.save()
        return instance
    