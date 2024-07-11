import requests
import pandas as pd
from io import StringIO
from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse

from .forms import UserForm

from .models import User, UserModification, Participant


def index(request):
    return render(request, 'user_profile/index.html')


@login_required()
def profile(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        old_first_name = user.first_name
        old_last_name = user.last_name
        old_email = user.email

        form = UserForm(request.POST or None, instance=user)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            new_first_name = cleaned_form["first_name"]
            new_last_name = cleaned_form["last_name"]
            new_email = cleaned_form["email"]

            user.first_name = new_first_name
            user.last_name = new_last_name
            user.email = new_email
            user.save()

            UserModification.objects.create(user=user,
                                            old_first_name=old_first_name,
                                            old_last_name=old_last_name,
                                            old_email=old_email,
                                            new_first_name=new_first_name,
                                            new_last_name=new_last_name,
                                            new_email=new_email,
                                            date_of_modification=datetime.now())
            return redirect(reverse("profile"))
    else:
        form = UserForm(instance=user)

    user.is_student = Participant.objects.filter(username=user.username).exists()
    user.save()

    modification = UserModification.objects.filter(user=user)
    date_of_modification = modification.latest("date_of_modification").date_of_modification.strftime("%Y-%m-%dT%H:%M:%S") if modification else None
    context = {"form": form, "username": user.username, "is_student": user.is_student, "date_of_modification": date_of_modification}
    return render(request, 'user_profile/profile.html', context)


def update_list_of_participants(request):
    participants_data = get_list_of_participants()
    list_of_new_participants_usernames = []

    for participant_data in participants_data:
        participant, created = Participant.objects.get_or_create(username=participant_data['username'])
        participant.enrolled_at = participant_data['enrolled_at']
        participant.save()

        if created:
            list_of_new_participants_usernames.append(participant.username)

    users = User.objects.filter(username__in=list_of_new_participants_usernames)
    users.update(is_student=True)
    return HttpResponse(_("Ok, database updated"), status=200)


def get_list_of_participants():
    url = "https://outreachdashboard.wmflabs.org/courses/Grupo_de_Usuários_Wiki_Movimento_Brasil/WikiConecta/users.json"
    response = requests.get(url)
    usernames = []
    try:
        data = response.json()
        user_dict_list = data["course"]["users"]
        usernames = [{"username": item["username"],
                      "enrolled_at": datetime.strptime(item["enrolled_at"], "%Y-%m-%dT%H:%M:%S.%fZ")}
                     for item in user_dict_list]
    except:
        pass
    return usernames


def login_oauth(request):
    return redirect(reverse('social:begin', kwargs={"backend": "mediawiki"}))


def logout(request):
    auth_logout(request)
    return redirect(reverse('homepage'))