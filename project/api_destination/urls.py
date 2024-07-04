from django.urls import path
from api_destination.views import *


urlpatterns = [
    path('destinations/',ListCreateDestination.as_view()),
    # accepts GET and POST requests Token required when POST 
    # path('categories/',ListCreateDestinationCategory.as_view()),
    path('destinations/<int:pk>/',DestinationDetails.as_view())
    # accepts GET, PUT, PATCH and DELETE requests Token required when editing or deleting 
]