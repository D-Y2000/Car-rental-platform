from django.urls import path
from .views import ExcursionOrganizerCreateView, ExcursionCreateView

urlpatterns = [
    path('excursion_organizers/', ExcursionOrganizerCreateView.as_view(), name='excursion-organizer-create'),
    path('excursions/', ExcursionCreateView.as_view(), name='excursion-create'),

]
