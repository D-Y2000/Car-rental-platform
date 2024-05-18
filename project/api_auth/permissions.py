from rest_framework import permissions
from api_agency.models import Notification





class CanReadNotification(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.user == request.user
