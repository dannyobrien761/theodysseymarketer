from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django import forms

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

def register_and_subscribe(request, plan_id):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # ✅ log them in
            return redirect('subscriptions:checkout', plan_id=plan_id)  # ✅ redirect to Stripe
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register_and_subscribe.html', {'form': form})


def account_home(request):
    return HttpResponse("User profile page")
    
def register_view(request):
    return HttpResponse("Register page")

def login_view(request):
    return HttpResponse("Logged in")

def logout_view(request):
    return HttpResponse("Logged out")