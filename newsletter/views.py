from django.shortcuts import render

# Create your views here.
# newsletter/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterForm
from utils.sendmail import send_email  # ← reuse your SendGrid helper

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)

            # Avoid duplicates (optional, already enforced by unique=True)
            if not form.Meta.model.objects.filter(email=subscriber.email).exists():
                subscriber.save()

                # Send confirmation email
                send_email(
                    to_email=subscriber.email,
                    subject="Welcome to the Impulsive Marketing Newsletter!",
                    html_content="""
                        <h2>Thanks for subscribing!</h2>
                        <p>You’ll now receive marketing insights, updates, and exclusive offers straight to your inbox.</p>
                        <p>- The Impulsive Marketing Team</p>
                    """
                )

                messages.success(request, "Thanks for subscribing to our newsletter!")
            else:
                messages.info(request, "You’re already subscribed!")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, "Please enter a valid email address.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = NewsletterForm()
    return render(request, 'newsletter/signup.html', {'form': form})
