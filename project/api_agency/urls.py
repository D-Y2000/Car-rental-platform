from django.urls import path
from api_agency.views import *
from rest_framework.authtoken.views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
urlpatterns = [
    path('login/',ObtainAuthToken.as_view(),),
    path('logout/',logOut),
    path('agencies/',Agencies.as_view()),
    path('agencies/<int:pk>/',AgencyDetails.as_view()),
    path('agency/profile/',agencyProfile),
    path('agencies/<int:pk>/branches/',AgencyBranches.as_view()),
    path('agency/branches/<int:pk>/',AgencyBranchesDetails.as_view()),
    path('agencies/<int:pk>/vehicles/',AgencyVehicles.as_view()),
    path('branches/',Branches.as_view()),
    path('branches/<int:pk>/',BranchDetails.as_view()),

    path('makes/',vehicles_makes),
    path('makes/<int:pk>/models/',vehicles_models),
    #search and filter view + creation
    path('vehicles/',ListVehicles.as_view()),
    path('vehicles/<int:pk>/',VehicleDetails.as_view()),

    #JWT VIEWS
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]