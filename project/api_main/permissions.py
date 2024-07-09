from rest_framework import permissions
from api_main.models import Profile
from api_agency.models import Agency,Reservation



class IsDefault(permissions.BasePermission):
    def has_permission(self, request, view):
        user=request.user
        
        return user.role == 'default'
    
class IsDefaultOrReadOly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user=request.user
        
        return user.role == 'default'
    

    
class IsProfileOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        #only profile owner can edit or delete
        user=request.user
        return obj.user == user


class CanEditResrvation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user=request.user
        return obj.client.user == user
    
class CandDeleteReservation(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.status == 'postponed'
    
class CanRateAndFeedback(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        profile = Profile.objects.get(user = user)
        agency_pk = view.kwargs.get('pk')
        try:
            agency = Agency.objects.get(pk=agency_pk)
        except Agency.DoesNotExist:
            return False
        reservations = Reservation.objects.filter(client = profile, agency = agency)
        if reservations:
            return True
        else:
            return False

class CanEditFeedback(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.user == user