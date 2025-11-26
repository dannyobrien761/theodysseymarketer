from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import SubscriptionPlan, Subscription
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import datetime
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

def subscriptions_home(request):
    return HttpResponse("Subscriptions app is working!")


@login_required
def subscription_success(request):
    return render(request, 'subscriptions/success.html')


def pricing_view(request):
    plans = SubscriptionPlan.objects.all()

    user_subscription = None
    if request.user.is_authenticated:
        user_subscription = Subscription.objects.filter(
            user=request.user, status='active'
        ).first()

    return render(request, 'subscriptions/pricing.html', {'plans': plans,
                  'user_subscription': user_subscription})


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
        success_url=request.build_absolute_uri('/subscriptions/success/') + '?success=true',
        cancel_url=request.build_absolute_uri('/subscriptions/pricing/'),
    )

    return redirect(session.url)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        print(f"⚠️ Webhook error: {e}")
        return HttpResponse(status=400)

    data = event['data']['object']
    event_type = event['type']

    # ✅ 1. When Checkout completes (new subscription created)
    if event_type == 'checkout.session.completed':
        customer_email = data.get('customer_email')
        stripe_sub_id = data.get('subscription')
        user = User.objects.filter(email=customer_email).first()

        if user and stripe_sub_id:
            try:
                sub = stripe.Subscription.retrieve(stripe_sub_id)
                price_id = sub['items']['data'][0]['price']['id']
                plan = SubscriptionPlan.objects.filter(stripe_price_id=price_id).first()

                subscription, created = Subscription.objects.update_or_create(
                    user=user,
                    defaults={
                        'stripe_subscription_id': stripe_sub_id,
                        'status': 'active',
                        'plan': plan,
                        'start_date': datetime.datetime.now()
                    }
                )
                print(f"✅ Subscription synced for {user.email} → Plan: {plan}")
            except Exception as e:
                print(f"❌ Webhook processing error (checkout.session.completed): {e}")

    # 🔄 2. When Subscription is updated (e.g., canceled or end date extended)
    elif event_type == 'customer.subscription.updated':
        stripe_sub_id = data.get('id')
        cancel_at_period_end = data.get('cancel_at_period_end')
        current_period_end = data.get('current_period_end')

        try:
            subscription = Subscription.objects.filter(stripe_subscription_id=stripe_sub_id).first()
            if subscription:
                # Set status
                subscription.status = 'canceled' if cancel_at_period_end else 'active'

                # Set end date (converted from Unix timestamp)
                if current_period_end:
                    subscription.end_date = datetime.datetime.fromtimestamp(current_period_end)

                # (Optional) update plan in case it changed
                price_id = data['items']['data'][0]['price']['id']
                plan = SubscriptionPlan.objects.filter(stripe_price_id=price_id).first()
                if plan:
                    subscription.plan = plan

                subscription.save()
                print(f"🔁 Updated subscription: {subscription.user.email} ({subscription.status})")

        except Exception as e:
            print(f"❌ Webhook processing error (subscription.updated): {e}")

    # ❌ 3. When a subscription is fully deleted (at end of billing cycle)
    elif event_type == 'customer.subscription.deleted':
        stripe_sub_id = data.get('id')
        subscription = Subscription.objects.filter(stripe_subscription_id=stripe_sub_id).first()
        if subscription:
            subscription.status = 'expired'
            subscription.save()
            print(f"❌ Subscription expired for: {subscription.user.email}")

    return HttpResponse(status=200)


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


@login_required
def billing_portal(request):
    subscription = Subscription.objects.filter(user=request.user).first()
    if not subscription:
        # fallback redirect if no active subscription
        return redirect('subscriptions:pricing')

    try:
        # Retrieve the Stripe customer via the subscription
        stripe_sub = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
        customer_id = stripe_sub.customer

        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=request.build_absolute_uri('/dashboard/'),
        )
        return redirect(session.url)
    except Exception as e:
        # Optionally add logging or user feedback
        print(f"⚠ Error creating billing portal session: {e}")
        return redirect('dashboard:dashboard-home')