from django.urls import path
from .views import (
    ExcursionOrganizerCreateView,
    ExcursionCreateView,
    ExcursionRetrieveUpdateView,
    ExcursionLocationCreateView,
)

urlpatterns = [
    path('excursion_organizers/', ExcursionOrganizerCreateView.as_view(), name='excursion-organizer-create'),
    path('', ExcursionCreateView.as_view(), name='excursion-create'),
    path('<str:pk>/', ExcursionRetrieveUpdateView.as_view(), name='excursion-retrieve-update'),
    path('<str:pk>/locations/', ExcursionLocationCreateView.as_view(), name='excursion-location-create'),

]
