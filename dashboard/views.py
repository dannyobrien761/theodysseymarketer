from django.shortcuts import render, redirect
from django.http import HttpResponse
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
        stripe_sub = stripe.Subscription.retrieve(subscription.stripe_subscription_id)

        # Get plan details
        plan_obj = stripe_sub['items']['data'][0]['plan']
        plan_id = plan_obj['id']
        plan_nickname = plan_obj.get('nickname', 'Unnamed Plan')

        # Get cancel/end date info
        cancel_at = stripe_sub.get('cancel_at_period_end', False)
        current_period_end = stripe_sub.get('current_period_end')

        if current_period_end:
            import datetime
            end_date = datetime.datetime.fromtimestamp(current_period_end).strftime('%Y-%m-%d')

        context = {
            'subscription': subscription,
            'plan_id': plan_id,
            'plan_nickname': plan_nickname,
            'cancel_at': cancel_at,
            'end_date': end_date,
        }

        return render(request, 'dashboard/home.html', context)

    else:
        # No active subscription; redirect or show message
        return redirect('subscriptions:pricing')

@login_required
def cancel_subscription(request):
    sub = Subscription.objects.filter(user=request.user, status='active').first()
    if sub and sub.stripe_subscription_id:
        try:
            stripe.Subscription.modify(
                sub.stripe_subscription_id,
                cancel_at_period_end=True
            )
            sub.status = 'canceled'
            sub.save()
            messages.success(request, "✅ Your subscription has been marked for cancellation at the end of the billing period.")
        except Exception as e:
            messages.error(request, f"⚠ Error canceling subscription: {e}")
    else:
        messages.warning(request, "⚠ No active subscription found to cancel.")
    return redirect('dashboard:dashboard-home')
