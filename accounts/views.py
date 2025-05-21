from django.shortcuts import render
from django.http import HttpResponse


def account_home(request):
    return HttpResponse("Accounts app is working!")
