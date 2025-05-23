from django.urls import path
from . import views
from subscriptions import views as subscription_views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.subscriptions_home, name='subscriptions-home'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('checkout/<uuid:plan_id>/', views.create_checkout_session, name='checkout'),
    path('webhooks/stripe/', subscription_views.stripe_webhook, name='stripe-webhook'),
]
