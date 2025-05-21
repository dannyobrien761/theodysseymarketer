from django.urls import path
from . import views

urlpatterns = [
    # temporary placeholder view
    path('', views.account_home, name='account-home'),
]