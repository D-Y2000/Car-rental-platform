from django.urls import path
from api_auth.views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
urlpatterns = [
        #JWT VIEWS
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/me/',UserProfile.as_view()),
    path('user/notifications/',UserListNotifications.as_view()),
    path('user/notifications/<int:pk>/',UserNotificationDetails.as_view()),
    ]
