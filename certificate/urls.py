from django.urls import path, include
from certificate import views

urlpatterns = [
    path('certificate/', views.certificate, name='certificate'),
    path('enrollment_letter/', views.enrollment_letter, name='enrollment_letter'),
    path('change_links/<str:next_url>', views.change_links, name='change_links'),
    path('manage_certificates/', views.manage_certificates, name='manage_certificates'),
    path('validate/', views.validate, name='validate_document')
]
