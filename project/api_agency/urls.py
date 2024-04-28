from django.urls import path
from api_agency.views import *

urlpatterns = [
    #Agency
    path('agencies/',Agencies.as_view()),
    path('agencies/<int:pk>/',AgencyDetails.as_view()),
    path('agency/profile/',agencyProfile),
    #agency overview(readonly)
    path('agency/overview/',agencyOverview),

    
    path('agencies/<int:pk>/branches/',AgencyBranches.as_view()),
    path('agency/branches/<int:pk>/',AgencyBranchesDetails.as_view()),
    path('agencies/<int:pk>/vehicles/',AgencyVehicles.as_view()),
    path('agencies/vehicle/images/<int:pk>/',VehicleImageDelete.as_view()),
    #Agency reservations
    path('agency/reservations/',ReservationList.as_view()),
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