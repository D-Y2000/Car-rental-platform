from django.urls import path
from api_destination.views import *


urlpatterns = [
    path('destinations/',ListCreateDestination.as_view()),
    # accepts GET and POST requests Token required when POST 
    # path('categories/',ListCreateDestinationCategory.as_view()),
    path('destinations/<int:pk>/',DestinationDetails.as_view()),
    # accepts GET, PUT, PATCH and DELETE requests Token required when editing or deleting 
    path('destinations/<int:pk>/rate/',RateDestination.as_view()),
    #Accepts POST request and create a rate for the destination with the given pk.
    path('destinations/<int:pk>/ratings/',DestinationsRatings.as_view()),
    #Acceptes GET request and returns the ratings of the destination with the given pk.
    path('destinations/<int:pk>/feedbacks/',FeedbackListCreate.as_view()),
    #Accepts POST request and create a feedback for the destination with the given pk.
    path('destinations/feedback/<int:pk>/',FeedbackDetails.as_view()),
    #Acceptes GET,PUT,PATCH and DELETE requests and returns the feedback the given pk.
    path('destinations/search_suggestions/',destinationssearchAutoComplete),
]