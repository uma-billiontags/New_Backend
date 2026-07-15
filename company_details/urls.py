from django.urls import path
from .  import views

urlpatterns = [
    path('create_client/', views.create_client, name='create_client'),
  ] 
