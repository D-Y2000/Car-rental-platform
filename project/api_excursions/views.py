from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    ExcursionOrganizer,
    Excursion,
    ExcursionLocation
)
from .serializers import (
    ExcursionOrganizerSerializer,
    ExcursionCreateSerializer,
    ExcursionUpdateSerializer,
    ExcursionLocationSerializer,
    ExcursionDetailSerializer,
)

class ExcursionOrganizerCreateView(generics.CreateAPIView):
    queryset = ExcursionOrganizer.objects.all()
    serializer_class = ExcursionOrganizerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ExcursionOrganizerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ExcursionOrganizer.objects.all()
    serializer_class = ExcursionOrganizerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ExcursionOrganizer.objects.filter(owner=user).first()


# Excursion creation following the initial step (see serializers.py)
class ExcursionCreateView(generics.CreateAPIView):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        organizer = ExcursionOrganizer.objects.get(owner=self.request.user)
        if not organizer:
            raise PermissionError('You must create an organizer profile first.')
        serializer.save(organizer=organizer)

# Excursion update following the second step (see serializers.py)
# -*- OR -*- Retrieve an excursion with its locations
class ExcursionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Excursion.objects.all()
    permission_classes = [IsAuthenticated]

    # hna nkhayro wchm serializer retrieve wella update apr n'jouter delete
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ExcursionUpdateSerializer
        return ExcursionDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Excursion.objects.filter(organizer__owner=user)

# Excursion update to add Locations (meeting points and destinations) to an existing excursion.
class ExcursionLocationCreateView(generics.CreateAPIView):
    queryset = ExcursionLocation.objects.all()
    serializer_class = ExcursionLocationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        excursion_id = self.kwargs.get('pk')
        print("owner>", self.request.user)
        print("excursion id>", excursion_id)

        excursion = Excursion.objects.filter(organizer__owner=self.request.user, id=excursion_id).first()
        print("excursion>", excursion)
        if not excursion:
            raise PermissionError("You do not have permission to add locations to this excursion.")
        serializer.save(excursion=excursion)

# Retrieve Organizer's excursions 
class ExcursionOrganizerExcursionsView(generics.ListAPIView):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionDetailSerializer
    permission_classes = [IsAuthenticated]
    print("ExcursionOrganizerExcursionsView")
    def get_queryset(self):
        user = self.request.user
        return Excursion.objects.filter(organizer__owner=user)
    
# retrieve authenticated user escursion organizer
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_excursion_organizer_by_user(request):
    user = request.user
    organizer = get_object_or_404(ExcursionOrganizer, owner=user)
    serializer = ExcursionOrganizerSerializer(organizer)
    return Response(serializer.data, status=status.HTTP_200_OK)