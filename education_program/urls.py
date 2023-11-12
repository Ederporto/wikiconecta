from django.urls import path
from education_program import views

urlpatterns = [
    path("insert/", views.insert_education_program, name='insert_education'),
    # path("add_institution/", views.insert_institution, name='insert_institution'),
]
