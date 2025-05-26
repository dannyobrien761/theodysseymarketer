from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard-home'),
    path('cancel/', views.cancel_subscription, name='cancel'),
]
