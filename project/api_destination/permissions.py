from rest_framework import permissions


class IsDestinationOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        #only profile owner can edit or delete
        user=request.user
        return obj.user == user
