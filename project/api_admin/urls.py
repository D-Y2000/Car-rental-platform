from django.urls import path
from api_admin.views import *


urlpatterns = [
    #views to manage users
    path('users/',AdminUserList.as_view()),
    path('users/<int:pk>/',AdminUserDetails.as_view()),
    #vieews to manage agencies.
    path('agencies/',AdminAgencyList.as_view()),
    path('agencies/<int:pk>/',AdminAgencyDetails.as_view()),
    path('agencies/<int:pk>/validate/',AdminValidateAgency.as_view()),
    #views to manage agencies ratings
    path('agencies/ratings/',AdminAgencyRatings.as_view()),
    path('agencies/ratings/<int:pk>/',AdminAgencyRatingsDetails.as_view()),#retreive and delete the rating
    #views to manage agencies feedbacks
    path('agencies/feedbacks/',AdminAgencyFeedbacks.as_view()),
    path('agencies/feedbacks/<int:pk>/',AdminAgencyFeedbacksDetails.as_view()),#retreive and delete the feedback
    #vieews to manage branches.
    path('branches/',AdminBranchList.as_view()),
    path('branches/<int:pk>/',AdminBranchDetails.as_view()),
    #views to manage vehicles
    path('vehicles/',AdminVehicleList.as_view()),
    path('vehicles/<int:pk>/',AdminVehicleDetails.as_view()),
    #views to manage Agencies Oreders
    path('reservations/',AdminReservationList.as_view()),
    path('reservations/<int:pk>/',AdminReservationDetails.as_view()),
    #views to manage Destinations
    path('destinations/',AdminDestinationList.as_view()),
    path('destinations/<int:pk>/',AdminDestinationDetails.as_view()),
    #views to manage destinations ratings
    path('destinations/ratings/',AdminDestinationRatings.as_view()),
    path('destinations/ratings/<int:pk>/',AdminDestinationRatingsDetails.as_view()),#retreive and delete the rating
    #views to manage destinations feedbacks
    path('destinations/feedbacks/',AdminDestinationFeedbacks.as_view()),
    path('destinations/feedbacks/<int:pk>/',AdminDestinationFeedbacksDetails.as_view()),#retreive and delete the feedback
    #views to manage Activities
    path('activities/',AdminActivityList.as_view()),
    path('activities/<int:pk>/',AdminActivityDetails.as_view()),
    #views to manage activities ratings
    path('activities/ratings/',AdminActivityRatings.as_view()),
    path('activities/ratings/<int:pk>/',AdminActivityRatingsDetails.as_view()),#retreive and delete the rating
    #views to manage activities feedbacks
    path('activities/feedbacks/',AdminActivityFeedbacks.as_view()),
    path('activities/feedbacks/<int:pk>/',AdminActivityFeedbacksDetails.as_view()),#retreive and delete the feedback
    


    
]