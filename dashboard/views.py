from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from subscriptions.models import Subscription
import stripe
from django.conf import settings
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
@login_required
def dashboard_home(request):
    subscription = Subscription.objects.filter(
        user=request.user, status__in=['active', 'canceled']
        ).first()

    if not subscription:
        return redirect('subscriptions:pricing')

    return render(request, 'dashboard/home.html', {'subscription': subscription})


@login_required
def cancel_subscription(request):
    sub = Subscription.objects.filter(user=request.user, status='active').first()

    if sub and sub.stripe_subscription_id:
        try:
            # Tell Stripe to cancel at period end
            stripe.Subscription.modify(
                sub.stripe_subscription_id,
                cancel_at_period_end=True
            )

            # Update local status immediately to 'canceled'
            sub.status = 'canceled'
            sub.save()

            messages.success(
                request,
                " Your subscription has been canceled and will remain active until the end of the current billing period."
            )

        except Exception as e:
            print(f" Error cancelling subscription: {e}")
            messages.error(
                request,
                " Something went wrong while trying to cancel your subscription. Please try again or contact support."
            )
    else:
        messages.warning(request, " No active subscription found to cancel.")

    return redirect('dashboard:dashboard-home')