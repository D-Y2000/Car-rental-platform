from django.urls import path
from api_agency.views import *
urlpatterns = [
    path('agencies/',agencies),
    path('agencies/<int:pk>/',agency_details),
    path('branches/',branches),
    path('branches/<int:pk>/',branch_details),
    path('agencies/<int:pk>/branches/',agency_branches),
    # path('makes/',vehicles_makes),
    # path('makes/<int:pk>',vehicles_models),
]