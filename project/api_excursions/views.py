from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ExcursionOrganizer, Excursion
from .serializers import ExcursionOrganizerSerializer, ExcursionCreateSerializer

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
    