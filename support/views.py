from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from .models import FAQ


def contact_view(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        reason = form.cleaned_data['reason']
        message = form.cleaned_data['message']

        subject = f"New Contact Form Submission: {reason}"
        body = f"From: {name} <{email}>\n\nReason: {reason}\n\nMessage:\n{message}"

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])

        messages.success(request, 'Your message has been sent! We’ll get back to you soon.')
        return redirect('support:contact')
    grouped = {
        label: FAQ.objects.filter(category=key)
        for key, label in FAQ.CATEGORY_CHOICES
    }

    return render(request, 'support/contact.html', {
        'form': form,
        'grouped_faqs': grouped,
    })
