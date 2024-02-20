from django.urls import path
from api_agency.views import *
from rest_framework.authtoken.views import *
urlpatterns = [
    path('agencies/',Agencies.as_view()),
    path('agencies/<int:pk>/',AgencyDetails.as_view()),
    path('branches/',Branches.as_view()),
    path('branches/<int:pk>/',BranchDetails.as_view()),
    path('agencies/<int:pk>/branches/',AgencyBranches.as_view()),

    # path('makes/',vehicles_makes),
    # path('makes/<int:pk>',vehicles_models),
    path('login/',ObtainAuthToken.as_view(),),
    path('logout/',logOut),

]