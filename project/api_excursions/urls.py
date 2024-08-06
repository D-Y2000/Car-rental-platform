from django.urls import path
from .views import (
    ExcursionOrganizerCreateView,
    ExcursionCreateView,
    ExcursionRetrieveUpdateView,
    ExcursionLocationCreateView,
    ExcursionOrganizerExcursionsView,
    PublishExcursionView,
    get_excursion_organizer_by_user,
    ExcursionListView,
    ChnageExcursionStatus,
    ExcursionOrganizerReadUpdateDelete,
    ExcursionMediaView
)

urlpatterns = [
    path('organizers/', ExcursionOrganizerCreateView.as_view(), name='excursion-organizer-create'),
    path('organizers/<int:pk>', ExcursionOrganizerReadUpdateDelete.as_view(), name='excursion-organizer-rud'),
    path('organizers/me/', get_excursion_organizer_by_user, name='excursion-organizer-retrieve'),
    path('organizers/excursions/', ExcursionOrganizerExcursionsView.as_view(), name='excursion-organizer-excursions'),
    path('', ExcursionCreateView.as_view(), name='excursion-create'),
    path('search/', ExcursionListView.as_view(), name='excursion-search'),
    path('<uuid:pk>/', ExcursionRetrieveUpdateView.as_view(), name='excursion-retrieve-update'),
    path('<uuid:pk>/locations/', ExcursionLocationCreateView.as_view(), name='excursion-location-create'),
    path('<uuid:pk>/publish/', PublishExcursionView.as_view(), name='publish-excursion'),
    path('<uuid:pk>/chnage-status/', ChnageExcursionStatus.as_view(), name='excursion-chnage-status'),
    path('<uuid:excursion_pk>/media/', ExcursionMediaView.as_view(), name='excursion-media'),  # Media endpoint    
]
