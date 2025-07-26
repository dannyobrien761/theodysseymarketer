from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from subscriptions.models import Subscription
import stripe
from django.conf import settings
from django.contrib import messages
import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def dashboard_home(request):
    subscription = Subscription.objects.filter(user=request.user).first()

    plan_name = None
    end_date = None
    cancel_at = None

    if subscription and subscription.stripe_subscription_id:
        try:
            stripe_sub = stripe.Subscription.retrieve(subscription.stripe_subscription_id)

            # Get plan details from Stripe
            plan_obj = stripe_sub['items']['data'][0]['plan']
            plan_name = plan_obj.get('nickname', None)  # e.g., "Starter Plan"

            # Fallback: use local SubscriptionPlan name if nickname is missing
            if not plan_name and subscription.plan:
                plan_name = subscription.plan.name

            # Get cancel/end date info
            cancel_at = stripe_sub.get('cancel_at_period_end', False)
            current_period_end = stripe_sub['items']['data'][0].get('current_period_end')

            if current_period_end:
                end_date = datetime.datetime.fromtimestamp(current_period_end).strftime('%Y-%m-%d')
            elif subscription.end_date:
                end_date = subscription.end_date.strftime('%Y-%m-%d')

        except Exception as e:
            print(f"⚠ Error loading Stripe subscription details: {e}")
            messages.warning(request, "Could not retrieve full subscription details.")

    context = {
        'subscription': subscription,
        'plan_name': plan_name,
        'cancel_at': cancel_at,
        'end_date': end_date,
    }

    print(f"Stripe subscription object: {stripe_sub}")
    print(f"cancel_at_period_end: {cancel_at}")
    print(f"current_period_end: {current_period_end}")

    return render(request, 'dashboard/home.html', context) if subscription else redirect('subscriptions:pricing')
