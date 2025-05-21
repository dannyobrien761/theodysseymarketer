from django.shortcuts import render
from django.shortcuts import render


def contact_view(request):
    return render(request, 'support/contact.html')
