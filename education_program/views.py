from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .forms import EducationProgramForm, ProfessorFormset, InstitutionFormset, UpdateInstitutionForm
from .models import EducationProgram, Institution, Professor
from .wiki import edit_page, build_states, build_mapframe, get_number_of_students_of_a_outreach_dashboard_program
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
            if program.link.startswith("https://outreachdashboard.wmflabs.org/courses/"):
                outreach_number = get_number_of_students_of_a_outreach_dashboard_program(program.link)
                if outreach_number:
                    program.number_students = outreach_number
            program.save()

        edit_page(request, settings.LIST_PAGE, build_states(), _("Adding or editing education program"))
        edit_page(request, settings.MAP_PAGE, build_mapframe(), _("Adding or editing education program"))
        return redirect("https://pt.wikiversity.org/wiki/WikiConecta")
    else:
        return render(request, "education_program/add_education_program.html", {
            'program_form': program_form,
            'professor_formset': professor_formset,
            'institution_formset': institution_formset
        })


@permission_required("education_program.change_educationprogram")
def update_education_program(request, education_program_id):
    program = get_object_or_404(EducationProgram, id=education_program_id)

    program_form = EducationProgramForm(request.POST or None, prefix='program', instance=program)
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
            if program.link.startswith("https://outreachdashboard.wmflabs.org/courses/"):
                outreach_number = get_number_of_students_of_a_outreach_dashboard_program(program.link)
                if outreach_number:
                    program.number_students = outreach_number
            program.save()

        edit_page(request, settings.LIST_PAGE, build_states(), _("Adding or editing education program"))
        edit_page(request, settings.MAP_PAGE, build_mapframe(), _("Adding or editing education program"))
        return redirect("https://pt.wikiversity.org/wiki/WikiConecta")
    else:
        return render(request, "education_program/update_education_program.html", {
            'program_form': program_form,
            'professor_formset': professor_formset,
            'institution_formset': institution_formset
        })


def list_education_programs(request):
    education_programs = EducationProgram.objects.all()
    context = {"programs": education_programs}
    return render(request, "education_program/list_education_programs.html", context)


@permission_required("education_program.change_institution")
def update_institution(request, institution_id):
    obj = get_object_or_404(Institution, id=institution_id)

    if request.method == "POST":
        institution_form = UpdateInstitutionForm(request.POST or None)
        if institution_form.is_valid():
            institution_form.save(institution_id=institution_id)
        context = {"institution": institution_form}
        return render(request, "education_program/update_institution.html", context)
    if request.method == "GET":
        institution_form = UpdateInstitutionForm(instance=obj)
        context = {"institution": institution_form}
        return render(request, "education_program/update_institution.html", context)


def update_pages(request):
    education_programs = EducationProgram.objects.all()

    for program in education_programs:
        if program.link.startswith("https://outreachdashboard.wmflabs.org/courses/"):
            outreach_number = get_number_of_students_of_a_outreach_dashboard_program(program.link)
            if outreach_number:
                program.number_students = outreach_number
                program.save()
    edit_page(request, settings.LIST_PAGE, build_states(), _("Adding or editing education program"))
    edit_page(request, settings.MAP_PAGE, build_mapframe(), _("Adding or editing education program"))
    return redirect("https://pt.wikiversity.org/wiki/" + settings.LIST_PAGE)


def list_institutions(request):
    institutions = Institution.objects.filter(education_program_institution__institution__isnull=False).distinct.order_by("name")
    context = {"institutions": institutions}
    return render(request, "education_program/list_education_programs_by_institution.html", context)


def list_professors(request):
    professors = Professor.objects.filter(education_program_professor__isnull=False).distinct.order_by("name")
    context = {"professors": professors}
    return render(request, "education_program/list_education_programs_by_professor.html", context)


def lang_ptbr_converter(lang):
    if lang == "pt-br" or lang == "pt":
        return "pt_BR"
    else:
        return lang
