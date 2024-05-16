from django.shortcuts import render
from api_auth.models import User
from api_auth.permissions import CanReadNotification
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api_auth.serializers import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework import generics
from rest_framework.views import APIView
from api_agency.models import Notification
from api_agency.serializers import NotifcationSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


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
    

#creat pair of tokens for autheticated user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    tokens =  {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return Response(tokens,status= status.HTTP_201_CREATED)

class ClientLogin(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email = email, password = password)
        if user :
            if user.role == 'default':
                return get_tokens_for_user(user)
        return Response('Account does not exist', status= status.HTTP_404_NOT_FOUND)
        

class AgencyLogin(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email = email, password = password)
        if user :
            if user.role == 'agency_admin':
                return get_tokens_for_user(user)
        return Response('Account does not exist', status= status.HTTP_404_NOT_FOUND)
        
            
