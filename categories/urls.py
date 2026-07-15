from django.urls import path
from . import views

urlpatterns = [
    
    # ── Login ──
    path('login_view/', views.login_view, name='login_view'),

    # ── Invoice Bank Details ──
    path('create_bank_detail/', views.create_bank_detail, name='create_bank_detail'),
    path('get_all_bank_details/', views.get_all_bank_details, name='get_all_bank_details'),
    path('get_bank_detail/<int:id>/', views.get_bank_detail, name='get_bank_detail'),
    path('edit_bank_detail/<int:id>/', views.edit_bank_detail, name='edit_bank_detail'),
    path('delete_bank_detail/<int:id>/', views.delete_bank_detail, name='delete_bank_detail'),

    # ── Invoice Company Address ──
    path('create_company_address/', views.create_company_address, name='create_company_address'),
    path('get_all_company_addresses/', views.get_all_company_addresses, name='get_all_company_addresses'),
    path('get_company_address/<int:id>/', views.get_company_address, name='get_company_address'),
    path('edit_company_address/<int:id>/', views.edit_company_address, name='edit_company_address'),
    path('delete_company_address/<int:id>/', views.delete_company_address, name='delete_company_address'),

    # ── Invoice Authorized Person ──
    path('create_authorized_person/', views.create_authorized_person, name='create_authorized_person'),
    path('get_all_authorized_persons/', views.get_all_authorized_persons, name='get_all_authorized_persons'),
    path('get_authorized_person/<int:id>/', views.get_authorized_person, name='get_authorized_person'),
    path('edit_authorized_person/<int:id>/', views.edit_authorized_person, name='edit_authorized_person'),
    path('delete_authorized_person/<int:id>/', views.delete_authorized_person, name='delete_authorized_person'),

    # ── Ads Formats ──
    path('create_ads_format/', views.create_ads_format, name='create_ads_format'),
    path('get_all_ads_formats/', views.get_all_ads_formats, name='get_all_ads_formats'),
    path('get_ads_format/<int:id>/', views.get_ads_format, name='get_ads_format'),
    path('edit_ads_format/<int:id>/', views.edit_ads_format, name='edit_ads_format'),
    path('delete_ads_format/<int:id>/', views.delete_ads_format, name='delete_ads_format'),

    # ── Metrics ──
    path('create_metric/', views.create_metric, name='create_metric'),
    path('get_all_metrics/', views.get_all_metrics, name='get_all_metrics'),
    path('get_metric/<int:id>/', views.get_metric, name='get_metric'),
    path('edit_metric/<int:id>/', views.edit_metric, name='edit_metric'),
    path('delete_metric/<int:id>/', views.delete_metric, name='delete_metric'),

    # ── Mode of Payment ──
    path('create_mode_of_payment/', views.create_mode_of_payment, name='create_mode_of_payment'),
    path('get_all_modes_of_payment/', views.get_all_modes_of_payment, name='get_all_modes_of_payment'),
    path('get_mode_of_payment/<int:id>/', views.get_mode_of_payment, name='get_mode_of_payment'),
    path('edit_mode_of_payment/<int:id>/', views.edit_mode_of_payment, name='edit_mode_of_payment'),
    path('delete_mode_of_payment/<int:id>/', views.delete_mode_of_payment, name='delete_mode_of_payment'),

    # ── Payment Terms ──
    path('create_payment_term/', views.create_payment_term, name='create_payment_term'),
    path('get_all_payment_terms/', views.get_all_payment_terms, name='get_all_payment_terms'),
    path('get_payment_term/<int:id>/', views.get_payment_term, name='get_payment_term'),
    path('edit_payment_term/<int:id>/', views.edit_payment_term, name='edit_payment_term'),
    path('delete_payment_term/<int:id>/', views.delete_payment_term, name='delete_payment_term'),

    # ── Ethnicity ──
    path('create_ethnicity/', views.create_ethnicity, name='create_ethnicity'),
    path('get_all_ethnicities/', views.get_all_ethnicities, name='get_all_ethnicities'),
    path('get_ethnicity/<int:id>/', views.get_ethnicity, name='get_ethnicity'),
    path('edit_ethnicity/<int:id>/', views.edit_ethnicity, name='edit_ethnicity'),
    path('delete_ethnicity/<int:id>/', views.delete_ethnicity, name='delete_ethnicity'),
    
    # ── Department ──
    path('create_department/', views.create_department, name='create_department'),
    path('get_all_departments/', views.get_all_departments, name='get_all_departments'),
    path('get_department/<int:id>/', views.get_department, name='get_department'),
    path('edit_department/<int:id>/', views.edit_department, name='edit_department'),
    path('delete_department/<int:id>/', views.delete_department, name='delete_department'),

    # ── Role ──
    path('create_role/', views.create_role, name='create_role'),
    path('get_all_roles/', views.get_all_roles, name='get_all_roles'),
    path('get_roles_by_department/<int:department_id>/', views.get_roles_by_department, name='get_roles_by_department'),
    path('get_role/<int:id>/', views.get_role, name='get_role'),
    path('edit_role/<int:id>/', views.edit_role, name='edit_role'),
    path('delete_role/<int:id>/', views.delete_role, name='delete_role'),
    
    # ── User Credentials ──
    path('create_user_credential/', views.create_user_credential, name='create_user_credential'),
    path('get_all_user_credentials/', views.get_all_user_credentials, name='get_all_user_credentials'),
    path('get_user_credential/<int:id>/', views.get_user_credential, name='get_user_credential'),
    path('edit_user_credential/<int:id>/', views.edit_user_credential, name='edit_user_credential'),
    path('delete_user_credential/<int:id>/', views.delete_user_credential, name='delete_user_credential'),
]