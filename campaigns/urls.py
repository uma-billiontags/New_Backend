from django.urls import path
from .  import views

urlpatterns = [
    path('create_campaign/', views.create_campaign, name='create_campaign'),
    path('get_campaigns/', views.get_campaigns, name='get_campaigns'),
]


# runserver: daphne CRM_Backend.asgi:application



