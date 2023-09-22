from django import forms
from .models import CourseModule, ActivityLink


class ActivityLinkForm(forms.ModelForm):
    class Meta:
        model = ActivityLink
        fields = ['link']
