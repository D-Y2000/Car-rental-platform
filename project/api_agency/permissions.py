from rest_framework import permissions
from api_agency.models import * 
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response


class IsAgency(permissions.BasePermission):
    def has_permission(self, request, view):
        user=User.objects.get(auth_token=request.auth)
        
        return user.role == 'agency_admin'


class IsAgencyOrReadOnly(permissions.BasePermission):    
    def has_object_permission(self, request, view, obj):
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        user=User.objects.get(auth_token=request.auth)
        return user.role=='agency_admin'
    

class IsAgencyOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        #only agency owner can edit or delete
        user=User.objects.get(auth_token=request.auth)
        return obj.user == user
    


class IsAgencyBranchOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):


        if request.method in permissions.SAFE_METHODS:
            return True
        
        user=User.objects.get(auth_token=request.auth)


        return obj.agency.user == user
    

class IsAgencyBranchOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user=User.objects.get(auth_token=request.auth)
        # print(obj.agency.user == user)
        return obj.agency.user == user