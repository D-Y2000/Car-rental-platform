from rest_framework import permissions
from api_agency.models import * 
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response

       
class IsAgencyOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == Token.objects.get(key=request.auth).user