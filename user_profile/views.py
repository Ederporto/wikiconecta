import requests
import pandas as pd
from io import StringIO
from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
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

    modification = UserModification.objects.filter(user=user)
    date_of_modification = modification.latest("date_of_modification").date_of_modification.strftime("%Y-%m-%dT%H:%M:%S") if modification else None
    context = {"form": form, "username": user.username, "is_student": user.is_student, "date_of_modification": date_of_modification}
    return render(request, 'user_profile/profile.html', context)


def update_list_of_participants(request):
    Participant.objects.all().delete()

    list_of_participants = [Participant(username=username) for username in get_list_of_participants()]
    Participant.objects.bulk_create(list_of_participants)
    return redirect(reverse("homepage"))


def get_list_of_participants():
    url = "https://outreachdashboard.wmflabs.org/course_students_csv"
    params = {"course": "Grupo_de_Usu%C3%A1rios_Wiki_Movimento_Brasil/WikiConecta"}

    response = requests.get(url, params=params)
    content = StringIO(response.content.decode())
    df = pd.read_csv(content)
    return list(df["username"])


def login_oauth(request):
    return redirect(reverse('social:begin', kwargs={"backend": "mediawiki"}))


def logout(request):
    auth_logout(request)
    return redirect(reverse('homepage'))