from django.shortcuts import render
from django.http import HttpResponse


def subscriptions_home(request):
    return HttpResponse("Subscriptions app is working!")
