from django.urls import path
from api_main.views import *
urlpatterns = [
    path('user/me/',UserProfile),
    path('profiles/',ProfileList.as_view()),
    path('profiles/<int:pk>/',ProfileDetails.as_view()),
    #client reservations
    path('profile/reservations/',MyReservations.as_view()),
    path('profile/reservations/<int:pk>/',Myreservation.as_view()),
]