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
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    event_type = event['type']
    data = event['data']['object']

    print(f" Received event: {event_type}")

    # New subscription via Checkout
    if event_type == 'checkout.session.completed':
        email = data.get('customer_email')
        stripe_sub_id = data.get('subscription')
        price_id = None

        # Get the price ID from the session line items
        line_items = stripe.checkout.Session.list_line_items(data['id'])
        if line_items['data']:
            price_id = line_items['data'][0]['price']['id']

        user = User.objects.filter(email=email).first()
        plan = SubscriptionPlan.objects.filter(stripe_price_id=price_id).first()

        if user and plan and stripe_sub_id:
            Subscription.objects.update_or_create(
                user=user,
                defaults={
                    'plan': plan,
                    'stripe_subscription_id': stripe_sub_id,
                    'status': 'active',
                }
            )
            print(" Subscription created for:", user.email)

    # Invoice Paid (for recurring renewals)
    elif event_type == 'invoice.paid':
        stripe_sub_id = data.get('subscription')
        sub = Subscription.objects.filter(stripe_subscription_id=stripe_sub_id).first()
        if sub:
            sub.status = 'active'
            sub.save()
            print(" Subscription renewed:", sub.user.email)

    #  Invoice Payment Failed
    elif event_type == 'invoice.payment_failed':
        stripe_sub_id = data.get('subscription')
        sub = Subscription.objects.filter(stripe_subscription_id=stripe_sub_id).first()
        if sub:
            sub.status = 'payment_failed'
            sub.save()
            print(" Payment failed for:", sub.user.email)

    # Subscription Cancelled
    elif event_type == 'customer.subscription.deleted':
        stripe_sub_id = data.get('id')
        sub = Subscription.objects.filter(stripe_subscription_id=stripe_sub_id).first()
        if sub:
            sub.status = 'cancelled'
            sub.save()
            print(" Subscription cancelled for:", sub.user.email)

    #  Subscription Updated (e.g. plan change)
    elif event_type == 'customer.subscription.updated':
        stripe_sub_id = data.get('id')
        sub = Subscription.objects.filter(stripe_subscription_id=stripe_sub_id).first()

        if sub:
            # Optional: update plan if changed
            items = data.get('items', {}).get('data', [])
            if items:
                price_id = items[0]['price']['id']
                plan = SubscriptionPlan.objects.filter(stripe_price_id=price_id).first()
                if plan:
                    sub.plan = plan
            sub.status = data.get('status', sub.status)
            sub.save()
            print(" Subscription updated:", sub.user.email)

    return HttpResponse(status=200)
