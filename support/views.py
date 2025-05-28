from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email (simplest)
            send_mail(
                subject=f"Contact Form Submission from {name}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent! We’ll get back to you soon.')
            return redirect('support:contact')
    else:
        form = ContactForm()

    return render(request, 'support/contact.html', {'form': form})
