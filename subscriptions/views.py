from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import SubscriptionPlan
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def subscriptions_home(request):
    return HttpResponse("Subscriptions app is working!")


def pricing_view(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/pricing.html', {'plans': plans})


def create_checkout_session(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='subscription',
        customer_email=request.user.email,
        line_items=[{
            'price': plan.stripe_price_id,
            'quantity': 1,
        }],
        success_url=request.build_absolute_uri('/dashboard/') + '?success=true',
        cancel_url=request.build_absolute_uri('/subscriptions/pricing/'),
    )

    return redirect(session.url)

