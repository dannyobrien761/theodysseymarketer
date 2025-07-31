from django.urls import path
from . import views
from subscriptions import views as subscription_views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.subscriptions_home, name='subscriptions-home'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('checkout/<uuid:plan_id>/', views.create_checkout_session, name='checkout'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('success/', views.subscription_success, name='success'),
    path('cancel/', views.cancel_subscription, name='cancel'),
    path('billing-portal/', views.billing_portal, name='billing-portal'),
]
