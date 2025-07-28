from django.db import models

# Create your models here.

# faq/models.py

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('billing', 'Billing'),
        ('features', 'Features'),
        ('technical', 'Technical'),
        ('general', 'General'),
    ]

    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question
