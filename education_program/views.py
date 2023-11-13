from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .forms import EducationProgramForm, ProfessorFormset, InstitutionFormset
from .models import EducationProgram
from .wiki import edit_page, build_states, build_mapframe
from django.utils.translation import gettext_lazy as _


@login_required
def insert_education_program(request):
    program_form = EducationProgramForm(request.POST or None, prefix='program')
    professor_formset = ProfessorFormset(request.POST or None, prefix='professor')
    institution_formset = InstitutionFormset(request.POST or None, prefix='institution')

    if request.method == "POST":
        professors_list = []
        institutions_list = []
        if professor_formset.is_valid():
            for professor_form in professor_formset:
                if professor_form.is_valid():
                    professor = professor_form.save()
                    professors_list.append(professor.id)
        if institution_formset.is_valid():
            for institution_form in institution_formset:
                if institution_form.is_valid():
                    institution = institution_form.save()
                    institutions_list.append(institution.id)
        if program_form.is_valid():
            program = program_form.save()
            program.professor.set(list(set(professors_list)))
            program.institution.set(list(set(institutions_list)))
            program.save()

        edit_page(request, settings.LIST_PAGE, build_states(), _("Adding or editing education program"))
        edit_page(request, settings.MAP_PAGE, build_mapframe(), _("Adding or editing education program"))
        return redirect("https://pt.wikiversity.org/wiki/WikiConecta")
    else:
        edit_page(request, settings.LIST_PAGE, build_states(), _("Adding or editing education program"))
        edit_page(request, settings.MAP_PAGE, build_mapframe(), _("Adding or editing education program"))
        return render(request, "education_program/add_education_program.html", {
            'program_form': program_form,
            'professor_formset': professor_formset,
            'institution_formset': institution_formset
        })


@permission_required("education_program.change_educationprogram")
def update_education_program(request, education_program_id):
    obj = get_object_or_404(EducationProgram, id=education_program_id)
    context = {}
    if request.method == "GET":
        program_form = EducationProgramForm(instance=obj, prefix='program')
        context = {
            "education_program": program_form
        }
    return render(request, "education_program/update_education_program.html", context)
