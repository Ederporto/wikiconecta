from django.contrib import admin
from .models import User, UserModification, Participant

admin.site.register(User)
admin.site.register(UserModification)
admin.site.register(Participant)
