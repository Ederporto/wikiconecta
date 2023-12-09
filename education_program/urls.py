from django.urls import path
from education_program import views

urlpatterns = [
    path("insert/", views.insert_education_program, name="insert_education_program"),
    path("list/", views.list_education_programs, name="list_education_programs"),
    path("list/by_institution", views.list_institutions, name="list_education_programs_by_institution"),
    path("list/by_professor", views.list_professors, name="list_education_programs_by_professor"),
    path("<int:education_program_id>/update", views.update_education_program, name="update_education_program"),
    path("institution/<int:institution_id>/update", views.update_institution, name="update_institution"),
    path("update_all", views.update_pages, name="update_all"),
    # path("add_institution/", views.insert_institution, name='insert_institution'),
]
