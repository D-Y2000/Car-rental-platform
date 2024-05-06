from django.urls import path
from api_agency.views import *

urlpatterns = [
    #Agency
    path('agencies/',Agencies.as_view()),
    path('agencies/<int:pk>/',AgencyDetails.as_view()),
    path('agency/profile/',agencyProfile),
    #agency overview(readonly)
    path('agency/overview/',agencyOverview),
    path('branch/<int:pk>/overview/',branchOverview),

    
    path('agencies/<int:pk>/branches/',AgencyBranches.as_view()),
    path('agency/branches/<int:pk>/',AgencyBranchesDetails.as_view()),
    path('agencies/<int:pk>/vehicles/',AgencyVehicles.as_view()),
    path('branches/<int:pk>/vehicles/',BranchVehicles.as_view()),
    path('agencies/vehicle/images/<int:pk>/',VehicleImageDelete.as_view()),
    #Agency reservations
    path('agency/reservations/',ReservationList.as_view()),
    # path('agency/reservations/?branch_pk',ReservationList.as_view()),
       #if the user is a branch admin then it'll return branch reservations
    #if the user is a agency admin then it'll return all  reservations related to the agency
    #if the parameter branch_pk is given in the url (agency/reservation/?branch_pk=<branch_pk>)
    #then it'll return the  reservations belonging to the branch with the specific pk of the agency
    path('agency/reservations/<int:pk>/',ReservationDetails.as_view()),
    path('agency/reservations/<int:pk>/accept/',AcceptReservation.as_view()),
    path('agency/reservations/<int:pk>/refuse/',RefuseReservation.as_view()),
    #Agency Ratings
    path('agencies/<int:pk>/rate/',RateAgency.as_view()),
    path('agencies/<int:pk>/ratings/',AgencyRatings.as_view()),

    #Branches
    path('branches/',Branches.as_view()),
    path('branches/<int:pk>/',BranchDetails.as_view()),
    #search and filter view + creation
    path('makes/',vehicles_makes),
    path('makes/<int:pk>/models/',vehicles_models),
    path('details/',get_details),
    path('wilayas/',get_wilayas),
    
    path('vehicles/',ListVehicles.as_view()),
    path('vehicles/<int:pk>/',VehicleDetails.as_view()),

]