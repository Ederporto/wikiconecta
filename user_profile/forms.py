from django import forms
from .models import User


class CustomTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'custom-text-input'}
        super().__init__(*args, **kwargs)


class CustomCheckboxInput(forms.CheckboxInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'custom-checkbox-input'}
        super().__init__(*args, **kwargs)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={"required": True}),
            'last_name': forms.TextInput(attrs={"required": True}),
            'email': forms.EmailInput(attrs={"required": True}),
        }

        def __init__(self, *args, **kwargs):
            instance = kwargs.get('instance', None)
            super().__init__(*args, **kwargs)

            if instance:
                self.fields["first_name"].initial = instance.first_name
                self.fields["last_name"].initial = instance.last_name
