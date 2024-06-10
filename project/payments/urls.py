from django.urls import path
from . import views

urlpatterns = [
    path('subscriptions/create/', views.create_subscription, name='create_subscription'),
    path('webhook/chargily/', views.webhook, name='webhook'),
    path('subscriptions/', views.list_subscriptions, name='list_subscriptions'),
]
