from django.urls import path
from api_main.views import *
urlpatterns = [
    path('profiles/', ProfileList.as_view()),
    path('profiles/account/', ProfileDetails.as_view()),
    # client reservations
    path('profile/reservations/', MyReservations.as_view()),
    path('profile/reservations/<int:pk>/', Myreservation.as_view()),
]
