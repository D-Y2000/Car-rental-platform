from django.urls import path
from api_activity.views import *


urlpatterns = [
    path('activities/',ListCtreateActivity.as_view()),
    # accepts GET and POST requests Token required when POST 
    # path('categories/',ListCreateActivityCategory.as_view()),
    path('activities/<int:pk>/',ActivityDetails.as_view()),
    # accepts GET, PUT, PATCH and DELETE requests Token required when editing or deleting 
    path('activities/<int:pk>/rate/',RateActivity.as_view()),
    #Accepts POST request and create a rate for the activity with the given pk.
    path('activities/<int:pk>/ratings/',ActivityRatings.as_view()),
    #Acceptes GET request and returns the ratings of the activity with the given pk.
    path('activities/<int:pk>/feedbacks/',FeedbackListCreate.as_view()),
    #Accepts POST request and create a feedback for the activity with the given pk.
    path('activities/feedback/<int:pk>/',FeedbackDetails.as_view()),
    #Acceptes GET,PUT,PATCH and DELETE requests and returns the feedback the given pk.
]