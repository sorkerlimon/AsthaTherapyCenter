from django.urls import path
from . import views
from . import views_admin

app_name = 'astha_therapy_center_web'

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('therapist/', views.therapist, name='therapist'),
    path('contact/', views.contact, name='contact'),
    path('appointment/', views.appointment, name='appointment'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog/', views.blog, name='blog'),
    path('faqs/', views.faqs, name='faqs'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('therapist/<uuid:therapist_id>/', views.therapist_single, name='therapist_single'),
    
    # SEO URLs
    path('sitemap.xml', views.sitemap, name='sitemap'),
    
    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Admin URLs
    path('therapy_admin/', views.therapy_admin, name='therapy_admin'),
    # Appointment Admin URLs
    path('therapy_admin/appointments/', views_admin.appointment_list, name='admin_appointment_list'),
    path('therapy_admin/appointments/create/', views_admin.appointment_create, name='admin_appointment_create'),
    path('therapy_admin/appointments/<uuid:appointment_id>/', views_admin.appointment_detail, name='admin_appointment_detail'),
    path('therapy_admin/appointments/<uuid:appointment_id>/edit/', views_admin.appointment_edit, name='admin_appointment_edit'),
    path('therapy_admin/appointments/<uuid:appointment_id>/delete/', views_admin.appointment_delete, name='admin_appointment_delete'),
    path('therapy_admin/appointments/<uuid:appointment_id>/update-status/', views_admin.appointment_update_status, name='admin_appointment_update_status'),
    # Contact Admin URLs
    path('therapy_admin/contacts/', views_admin.contact_list, name='admin_contact_list'),
    path('therapy_admin/contacts/<uuid:contact_id>/', views_admin.contact_detail, name='admin_contact_detail'),
    path('therapy_admin/contacts/<uuid:contact_id>/edit/', views_admin.contact_edit, name='admin_contact_edit'),
    path('therapy_admin/contacts/<uuid:contact_id>/delete/', views_admin.contact_delete, name='admin_contact_delete'),
    path('therapy_admin/contacts/<uuid:contact_id>/update-status/', views_admin.contact_update_status, name='admin_contact_update_status'),
    
    # Therapist Admin URLs
    path('therapy_admin/therapists/', views_admin.therapist_list, name='admin_therapist_list'),
    path('therapy_admin/therapists/create/', views_admin.therapist_create, name='admin_therapist_create'),
    path('therapy_admin/therapists/<uuid:therapist_id>/', views_admin.therapist_detail, name='admin_therapist_detail'),
    path('therapy_admin/therapists/<uuid:therapist_id>/edit/', views_admin.therapist_edit, name='admin_therapist_edit'),
    path('therapy_admin/therapists/<uuid:therapist_id>/delete/', views_admin.therapist_delete, name='admin_therapist_delete'),
    path('therapy_admin/therapists/<uuid:therapist_id>/update-status/', views_admin.therapist_update_status, name='admin_therapist_update_status'),
]
