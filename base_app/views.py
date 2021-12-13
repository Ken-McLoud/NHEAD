from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, "base_app/base.html", context={"message": "hellos worlds"})
