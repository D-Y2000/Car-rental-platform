from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/agency/',include('api_agency.urls')),
    path('api/main/',include('api_main.urls')),
    path('api/auth/',include('api_auth.urls')),
    path('api/payment/',include('payments.urls')),
    path('api/destination/',include('api_destination.urls')),
    path('api/activity/',include('api_activity.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)