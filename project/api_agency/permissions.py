from django.utils import timezone
from rest_framework import permissions
from api_agency.models import Agency, Branch, Plan
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
    def has_permission(self, request, view):
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        #only agency can add vehicle
        user=request.user
        agency  = Agency.objects.get(user=user)
        subscription = agency.my_new_subscriptions.order_by('-created_at').first()
        if subscription and subscription.end_at > timezone.now():
            return True
        else:
            free_plan = Plan.objects.get(name = "free")
            if agency.my_branches.count()< free_plan.max_branches:
                return True
        return False


class CanRudBranches(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #only the agency owner of the current branch can edit or delete
        user=request.user


        return obj.agency.user == user and obj.is_locked == False
    

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


class CanCreateVehicle(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        #only agency can add vehicle
        try:
            user=request.user
            agency  = Agency.objects.get(user=user)
            branch = Branch.objects.get(pk=request.data.get('owned_by'))
            subscription = agency.my_new_subscriptions.order_by('-created_at').first()
            if subscription and subscription.end_at > timezone.now():
                return True
            else:
                free_plan = Plan.objects.get(name = "free")
                if branch.my_vehicles.count()< free_plan.max_vehicles:
                    return True
            return False
        except Branch.DoesNotExist:
            return False

class CanRudVehicles(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # only the user of the agency that owns this vehicle can edit or delete
        user=request.user
        return obj.owned_by.agency.user==user and obj.is_locked == False
    

class CanRudReservation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user=request.user
        return obj.branch.agency.user == user

class CanDestroyVehicleImage(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user=request.user
        return obj.vehicle.owned_by.agency.user==user
    


class IsPro(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        agency = Agency.objects.get(user = user)
        return agency.mys_subscriptions.first().plan == 'Pro'
    