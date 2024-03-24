from django.shortcuts import render
from api_auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api_auth.serializers import *
from rest_framework.decorators import api_view,permission_classes
# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfile(request):
    user=request.user
    user=User.objects.get(email=user.email)
    serializer=UserDetailsSerializer(user)
    return Response(serializer.data,status=status.HTTP_200_OK)
