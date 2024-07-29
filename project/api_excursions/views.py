from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
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