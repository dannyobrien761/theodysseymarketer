from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return [
            'core:home',
            'core:how_it_works',
            'subscriptions:pricing',
            'support:contact',
            'support:faq',
        ]

    def location(self, item):
        return reverse(item)
