from rest_framework import permissions
from api_agency.models import Agency, Branch 
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response

class IsAgency(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        
        return user.role == 'agency_admin'



class IsAgencyOrReadOnly(permissions.BasePermission):    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user=request.user
        return user.role =='agency_admin'
    

class IsAgencyOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        #only agency owner can edit or delete
        user=request.user
        return obj.user == user
    
    
class CanCreateBranches(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        #only agency can add vehicle
        user=request.user
        return user.role =='agency_admin'


class CanRudBranches(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        #only the agency owner of the current branch can edit or delete
        user=request.user


        return obj.agency.user == user
    

class IsBranchOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user=request.user
        agency=Agency.objects.get(user=user)
        branches=Branch.objects.filter(agency=agency)
        if branches.exists():
            return True
        else:
            return False




class CanRudVehicles(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # only the user of the agency that owns this vehicle can edit or delete
        user=request.user
        return obj.owned_by.agency.user==user
    

class CanRudReservation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user=request.user
        return obj.branch.agency.user == user

class CanDestroyVehicleImage(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user=request.user
        return obj.vehicle.owned_by.agency.user==user