from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'core/home.html')

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow:",
        f"Sitemap: https://marketing-agency-fcc8243e8eeb.herokuapp.com/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")