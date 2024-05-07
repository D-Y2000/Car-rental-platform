from django.urls import path
from api_agency.views import *

urlpatterns = [
    #Agency
   
    path('agencies/',Agencies.as_view()),
    #This endpoint accept GET and POST requests for Listing and creating new agencies. 
    path('agencies/<int:pk>/',AgencyDetails.as_view()),
    #This endpoint accepts GET,PUT,PATCH and DELETE requests to retreive,update and destroy agency object.
    path('agency/profile/',agencyProfile),
    #Accepts GET request and return the logged in agency profile.
    path('agency/overview/',agencyOverview),
    #agency overview(readonly) it accepts GET request and returns the agency with branches and reservations.
    path('branch/<int:pk>/overview/',branchOverview),
    #agency overview(readonly) it accepts GET request and returns the branch with vehicles  and reservations.
    path('agencies/<int:pk>/branches/',AgencyBranches.as_view()),
    #Acceptes GET requests and returns agency branches list  
    path('agency/branches/<int:pk>/',AgencyBranchesDetails.as_view()),
    #Acceptes GET,PUT,PATCH and DELETE requests and returns agencys branch with the given pk and  edit or delete the branch object. 
    path('agencies/<int:pk>/vehicles/',AgencyVehicles.as_view()),
    #Accepts GET request and returns the vehicles specifc to each branch related to the agency with the given pk.
    path('branches/<int:pk>/vehicles/',BranchVehicles.as_view()),
    #Accepts GET request and return the vehicles specific to the branch with given pk.
    path('agencies/vehicle/images/<int:pk>/',VehicleImageDelete.as_view()),
    #Accepts DELETE request and delete the vehicle image with the given pk.
    path('agency/reservations/',ReservationList.as_view()),
    #Accepts GET request.
    #path('agency/reservations/?branch_pk',ReservationList.as_view()),
    #if the user is a branch admin then it'll return branch reservations
    #if the user is a agency admin then it'll return all  reservations related to the agency
    #if the parameter branch_pk is given in the url (agency/reservation/?branch_pk=<branch_pk>)
    #then it'll return the  reservations belonging to the branch with the specific pk of the agency
    path('agency/reservations/<int:pk>/',ReservationDetails.as_view()),
    #Accepts GET request and returns the reservation with the given pk.
    path('agency/reservations/<int:pk>/accept/',AcceptReservation.as_view()),
    #Accepts PUT,PATCH requests and edits the satatus of the reservation to accepted
    path('agency/reservations/<int:pk>/refuse/',RefuseReservation.as_view()),
    #Accepts PUT,PATCH requests and edit the satatus of the reservation to refused
    #Agency Ratings
    path('agencies/<int:pk>/rate/',RateAgency.as_view()),
    #Accepts POST request and create a rate for the agency with the given pk.
    path('agencies/<int:pk>/ratings/',AgencyRatings.as_view()),
    #Acceptes GET request and returns the ratings of the agency with the given pk.

    #Branches
    path('branches/',Branches.as_view()),
    #Accepts GET,POST requests and creates a new branch or list all existing branches.
    path('branches/<int:pk>/',BranchDetails.as_view()),
    #Accepts GET request and returns the branch with the given pk.

    path('vehicles/',ListVehicles.as_view()),
    #Accepts GET,POST requests and creates a new vehicle or list all existing vehicles ,search and filter.
    path('vehicles/<int:pk>/',VehicleDetails.as_view()),
     #This endpoint accepts GET,PUT,PATCH and DELETE requests to retreive,update and destroy vehicle with the given pk.

    path('makes/',vehicles_makes),
    #Accepts GET request and returns all gthe existing makes.
    path('makes/<int:pk>/models/',vehicles_models),
    #Accepts GET request and returns all gthe existing models related to the make with the given pk.
    path('details/',get_details),
    #Accepts GET request and returns data about vehicles (types,energies,transsmission and options). 
    path('wilayas/',get_wilayas),
    #Accepts GET request and returns all existing wilayas.
     

]