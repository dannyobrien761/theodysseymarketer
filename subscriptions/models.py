from django.db import models
from django.conf import settings
import uuid


class SubscriptionPlan(models.Model):

    BILLING_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CHOICES)
    features = models.JSONField(default=dict)  # flexible list of features
    stripe_price_id = models.CharField(max_length=255, help_text="Stripe Price ID")

    def __str__(self):
        return f"{self.name} ({self.billing_cycle})"


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    stripe_subscription_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"
