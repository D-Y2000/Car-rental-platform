from django.urls import path
from api_agency.views import *
from rest_framework.authtoken.views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
urlpatterns = [
    #JWT VIEWS
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #Agency
    path('agencies/',Agencies.as_view()),
    path('agencies/<int:pk>/',AgencyDetails.as_view()),
    path('agency/profile/',agencyProfile),
    path('agencies/<int:pk>/branches/',AgencyBranches.as_view()),
    path('agency/branches/<int:pk>/',AgencyBranchesDetails.as_view()),
    path('agencies/<int:pk>/vehicles/',AgencyVehicles.as_view()),
    #Agency reservations
    path('agency/reservations/',ReservationList.as_view()),
    path('agency/reservations/<int:pk>/',ReservationDetails.as_view()),
    #Branches
    path('branches/',Branches.as_view()),
    path('branches/<int:pk>/',BranchDetails.as_view()),
    #search and filter view + creation
    path('makes/',vehicles_makes),
    path('makes/<int:pk>/models/',vehicles_models),

    
    path('vehicles/',ListVehicles.as_view()),
    path('vehicles/<int:pk>/',VehicleDetails.as_view()),

    
]