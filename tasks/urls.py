from django.urls import path
from . import views

urlpatterns = [
    path('get_department_users/<str:department_title>/', views.get_department_users, name='get_department_users'),
    path('assign_task/', views.assign_task, name='assign_task'),
    path('mark_task_complete/<int:task_id>/', views.mark_task_complete, name='mark_task_complete'),
    path('get_assignments_for_tickets/', views.get_assignments_for_tickets, name='get_assignments_for_tickets'),
    path('get_my_leads/', views.get_my_leads, name='get_my_leads'),
    path('get_ticket_task_history/<str:ticket_id>/', views.get_ticket_task_history, name='get_ticket_task_history'), 
    path('get_assignment_history_for_tickets/', views.get_assignment_history_for_tickets, name='get_assignment_history_for_tickets'),
    path('get_status_report/', views.get_status_report, name='get_status_report'),
]