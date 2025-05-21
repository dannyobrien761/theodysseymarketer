from django.shortcuts import render
from django.http import HttpResponse


def subscriptions_home(request):
    return HttpResponse("Subscriptions app is working!")


def pricing_view(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/pricing.html', {'plans': plans})
