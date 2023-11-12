from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EducationProgramForm, ProfessorFormset, InstitutionFormset
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

        edit_page(settings.LIST_PAGE, build_states(), _("Adding or editing education program"))
        edit_page(settings.MAP_PAGE, build_mapframe(), _("Adding or editing education program"))
        return redirect("https://pt.wikiversity.org/wiki/WikiConecta")
    else:
        return render(request, "education_program/add_education_program.html", {
            'program_form': program_form,
            'professor_formset': professor_formset,
            'institution_formset': institution_formset
        })
