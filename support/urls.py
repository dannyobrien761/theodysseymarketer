from django.urls import path
from . import views
from .views import faq_list_grouped

app_name = 'support'

urlpatterns = [
    path('contact/', views.contact_view, name='contact'),
    path('', faq_list_grouped, name='faq'),
]
