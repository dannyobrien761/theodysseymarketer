from django.shortcuts import render
from django.http import HttpResponse


def payments_home(request):
    return HttpResponse("Payments app is working!")
