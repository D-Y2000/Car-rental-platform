from django.urls import path
from api_agency import views

urlpatterns = [
    #Agency
   
    path('agencies/', views.Agencies.as_view()),
    #This endpoint accept GET and POST requests for Listing and creating new agencies. 
    path('agencies/<int:pk>/',views.AgencyDetails.as_view()),
    #This endpoint accepts GET,PUT,PATCH and DELETE requests to retreive,update and destroy agency object.
    path('agency/profile/',views.agencyProfile),
    #Accepts GET request and return the logged in agency profile.
    path('agency/overview/',views.agencyOverview),
    #agency overview(readonly) it accepts GET request and returns the agency with branches and reservations.
    path('branch/<int:pk>/overview/',views.branchOverview),
    #agency overview(readonly) it accepts GET request and returns the branch with vehicles  and reservations.
    path('agencies/<int:pk>/branches/',views.AgencyBranches.as_view()),
    #Acceptes GET requests and returns agency branches list  
    path('agency/branches/<int:pk>/',views.AgencyBranchesDetails.as_view()),
    #Acceptes GET,PUT,PATCH and DELETE requests and returns agencys branch with the given pk and  edit or delete the branch object. 
    path('agencies/<int:pk>/vehicles/',views.AgencyVehicles.as_view()),
    #Accepts GET request and returns the vehicles specifc to each branch related to the agency with the given pk.
    path('branches/<int:pk>/vehicles/',views.BranchVehicles.as_view()),
    #Accepts GET request and return the vehicles specific to the branch with given pk.
    path('agencies/vehicle/images/<int:pk>/',views.VehicleImageDelete.as_view()),
    #Accepts DELETE request and delete the vehicle image with the given pk.
    path('agency/reservations/',views.ReservationList.as_view()),
    #Accepts GET request.
    #path('agency/reservations/?branch_pk',ReservationList.as_view()),
    #if the user is a branch admin then it'll return branch reservations
    #if the user is a agency admin then it'll return all  reservations related to the agency
    #if the parameter branch_pk is given in the url (agency/reservation/?branch_pk=<branch_pk>)
    #then it'll return the  reservations belonging to the branch with the specific pk of the agency
    path('agency/reservations/<int:pk>/',views.ReservationDetails.as_view()),
    #Accepts GET request and returns the reservation with the given pk.
    path('agency/reservations/<int:pk>/accept/',views.AcceptReservation.as_view()),
    #Accepts PUT,PATCH requests and edits the satatus of the reservation to accepted
    path('agency/reservations/<int:pk>/refuse/',views.RefuseReservation.as_view()),
    #Accepts PUT,PATCH requests and edit the satatus of the reservation to refused
    #Agency Ratings
    path('agencies/<int:pk>/rate/',views.RateAgency.as_view()),
    #Accepts POST request and create a rate for the agency with the given pk.
    path('agencies/<int:pk>/ratings/',views.AgencyRatings.as_view()),
    #Acceptes GET request and returns the ratings of the agency with the given pk.
    #Agency Feedbacks
    path('agencies/<int:pk>/feedbacks/',views.FeedbackListCreate.as_view()),
    #Accepts POST request and create a feedback for the agency with the given pk.
    path('agencies/feedback/<int:pk>/',views.FeedbackDetails.as_view()),
    #Acceptes GET,PUT,PATCH and DELETE requests and returns the feedback the given pk.
    path('agency/subscribe/',views.AgencySubscription.as_view()),
    #Branches
    path('branches/',views.Branches.as_view()),
    #Accepts GET,POST requests and creates a new branch or list all existing branches.
    path('branches/<int:pk>/',views.BranchDetails.as_view()),
    #Accepts GET request and returns the branch with the given pk.

    path('vehicles/',views.ListVehicles.as_view()),
    #Accepts GET,POST requests and creates a new vehicle or list all existing vehicles ,search and filter.
    path('nearby_vehicles/',views.NearbyVehicles.as_view()),
    #Accepts GET, and the parametres lat,long for user position and the raduis
    path('vehicles/<int:pk>/',views.VehicleDetails.as_view()),
     #This endpoint accepts GET,PUT,PATCH and DELETE requests to retreive,update and destroy vehicle with the given pk.

    path('makes/',views.vehicles_makes),
    #Accepts GET request and returns all gthe existing makes.
    path('makes/<int:pk>/models/',views.vehicles_models),
    #Accepts GET request and returns all gthe existing models related to the make with the given pk.
    path('details/',views.get_details),
    #Accepts GET request and returns data about vehicles (types,energies,transsmission and options). 
    path('wilayas/',views.get_wilayas),
    #Accepts GET request and returns all existing wilayas.
     
    # get Plans
    path('plans/',views.get_plans),

    #reports
    path('agencies/<int:pk>/report/',views.ReportAgency.as_view()),
    #Accepts POST request to report the agency with the given pk.

    path('reports/',views.ReportList.as_view()),

    path('agency/reservations/stats', views.reservations_stats, name='reservations_stats'),


]