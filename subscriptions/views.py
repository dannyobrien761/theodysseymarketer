from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import SubscriptionPlan, Subscription
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User





stripe.api_key = settings.STRIPE_SECRET_KEY


def subscriptions_home(request):
    return HttpResponse("Subscriptions app is working!")



def pricing_view(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/pricing.html', {'plans': plans})

@login_required
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


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe Webhooks for subscription billing"""

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    event_type = event['type']
    data = event['data']['object']

    if event['type'] == 'checkout.session.completed':
        data = event['data']['object']
        stripe_sub_id = data.get('subscription')
        customer_email = data.get('customer_email')

        user = User.objects.filter(email=customer_email).first()

        if user and stripe_sub_id:
            Subscription.objects.get_or_create(
                user=user,
                stripe_subscription_id=stripe_sub_id,
                defaults={'status': 'active'}
            )

    elif event_type == 'invoice.payment_failed':
        stripe_sub_id = data.get('subscription')
        subscription = Subscription.objects.filter(stripe_subscription_id=stripe_sub_id).first()

        if subscription:
            subscription.status = 'payment_failed'
            subscription.save()
            print(f" Payment failed for {subscription.user.email}")


    return HttpResponse(status=200)
