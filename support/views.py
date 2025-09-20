from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings
from .models import FAQ
from utils.send_email import send_email


def contact_view(request):
    form = ContactForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        reason = form.cleaned_data['reason']
        message = form.cleaned_data['message']

        subject = f"New Contact Form Submission: {reason}"
        html_content = f"""
            <p><strong>From:</strong> {name} ({email})</p>
            <p><strong>Reason:</strong> {reason}</p>
            <p><strong>Message:</strong><br>{message}</p>
        """

        status = send_email(
            subject=subject,
            to_email=settings.DEFAULT_FROM_EMAIL,
            html_content=html_content,
        )

        if status == 202:
            messages.success(request, 'Your message has been sent! We’ll get back to you soon.')
        else:
            messages.error(request, 'There was an error sending your message. Please try again.')

        return redirect('support:contact')

    grouped = {
        label: FAQ.objects.filter(category=key)
        for key, label in FAQ.CATEGORY_CHOICES
    }

    return render(request, 'support/contact.html', {
        'form': form,
        'grouped_faqs': grouped,
    })