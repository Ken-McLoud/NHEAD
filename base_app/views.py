from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import CreateUserForm


def home(request):
    return render(request, "base_app/home.html")


def create_user_view(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            """
            #example for adding another field
            user.userprofilemodel.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            """
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("base_app:home")
    else:
        form = CreateUserForm()
    return render(
        request,
        "accounts/register.html",
        {"form": form, "title": "Create New Account"},
    )


def testview(request):
    return render(request, "base_app/non_crispy_form.html")
