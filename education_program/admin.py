from django.contrib import admin
from .models import Professor, Institution, EducationProgram

admin.site.register(Professor)
admin.site.register(Institution)
admin.site.register(EducationProgram)
