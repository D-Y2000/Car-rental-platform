from django.urls import path
from api_agency.views import *
from rest_framework.authtoken.views import *
urlpatterns = [
    path('agencies/',agencies.as_view()),
    path('agencies/<int:pk>/',agency_details.as_view()),
    path('branches/',branches),
    path('branches/<int:pk>/',branch_details),
    path('agencies/<int:pk>/branches/',agency_branches),
    # path('makes/',vehicles_makes),
    # path('makes/<int:pk>',vehicles_models),
    path('login/',ObtainAuthToken.as_view(),),
    path('logout/',logOut)
]