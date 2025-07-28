from django.contrib import admin
from .models import FAQ

# Register your models here.
# faq/admin.py


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('question', 'answer')
