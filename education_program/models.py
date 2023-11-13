from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.conf import settings
from datetime import datetime


class Institution(models.Model):
    name = models.CharField(_("Institution or University name"), max_length=280)
    postal_code = models.CharField(_("Postal code"), max_length=20)
    state = models.CharField(_("State"), max_length=2, choices=settings.STATES, blank=True)
    city = models.CharField(_("City"), max_length=280, blank=True)
    lat = models.FloatField(_("Latitude"), null=True, blank=True)
    lon = models.FloatField(_("Longitude"), null=True, blank=True)

    def __str__(self):
        if self.city:
            return self.name + " (" + self.city + ")"
        else:
            return self.name


class Professor(models.Model):
    name = models.CharField(_("Name"), max_length=280)
    username = models.CharField(_("Wikimedia username"), max_length=280, null=True, blank=True)

    def __str__(self):
        if self.username:
            return self.name + " (" + self.username + ")"
        else:
            return self.name


class EducationProgram(models.Model):
    MODALITY = (
        ("in_person", _("In person")),
        ("hybrid", _("Hybrid")),
        ("online", _("Online")),
    )
    name = models.CharField(_("Course name"), max_length=280)
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"))
    link = models.URLField(_("Link"), null=True, blank=True)
    course_type = models.CharField(_("Course type"), choices=MODALITY, max_length=10, default=None)
    institution = models.ManyToManyField(Institution, verbose_name=_("Institution"), related_name="education_program_institution")
    professor = models.ManyToManyField(Professor, verbose_name=_("Professor"), related_name="education_program_professor")
    number_students = models.IntegerField(_("Number of students or participants"), blank=True, null=True,
                                          validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name + " (" + self.start_date.strftime("%m/%d/%Y") + "-" + self.end_date.strftime("%m/%d/%Y") + ")"
