from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from subscriptions.models import Subscription
import stripe
from django.conf import settings
from django.contrib import messages


@login_required
def dashboard_home(request):
    subscription = Subscription.objects.filter(user=request.user, status='active').first()
    if not subscription:
        return redirect('subscriptions:pricing')
    return render(request, 'dashboard/home.html', {'subscription': subscription})


@login_required
def cancel_subscription(request):
    sub = Subscription.objects.filter(user=request.user).first()
    if sub and sub.stripe_subscription_id:
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.Subscription.delete(sub.stripe_subscription_id)
            sub.status = 'cancelled'
            sub.save()
            messages.success(request, "Your subscription has been cancelled.")
        except Exception as e:
            messages.error(request, "Something went wrong while cancelling.")
    return redirect('dashboard:home')