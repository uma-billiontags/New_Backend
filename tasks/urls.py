from django.urls import path
from . import views

urlpatterns = [
    path('get_department_users/<str:department_title>/', views.get_department_users, name='get_department_users'),
    path('assign_task/', views.assign_task, name='assign_task'),
    path('get_assignments_for_tickets/', views.get_assignments_for_tickets, name='get_assignments_for_tickets'),
    path('get_my_leads/', views.get_my_leads, name='get_my_leads'),
]