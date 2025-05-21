from django.shortcuts import render
from django.http import HttpResponse


def account_home(request):
    return HttpResponse("User profile page")

def register_view(request):
    return HttpResponse("Register page")

def login_view(request):
    return HttpResponse("Logged in")

def logout_view(request):
    return HttpResponse("Logged out")
