from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.subscriptions_home, name='subscriptions-home'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('checkout/<uuid:plan_id>/', views.create_checkout_session, name='checkout'),
]
