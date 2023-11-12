from django.contrib import admin
from .models import ActivityLink, Certificate, CourseModule

admin.site.register(ActivityLink)
admin.site.register(Certificate)
admin.site.register(CourseModule)