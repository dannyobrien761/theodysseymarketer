"""marketing_agency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['core:home', 'core:how_it_works', 'subscriptions:pricing', 'support:contact']

    def location(self, item):
        return reverse(item)

sitemaps = {
    'static': StaticViewSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('allauth.urls')),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('payments/', include('payments.urls')),
    path('support/', include('support.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]
