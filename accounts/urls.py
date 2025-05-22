from django.urls import path
from . import views

app_name = 'accounts' 

urlpatterns = [
    path('register/<uuid:plan_id>/', views.register_and_subscribe, name='register'),
]
