# gregdyche/urls.py

"""
URL configuration for gregdyche project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from blog.models import Page

# This function must be defined to be used below
def home(request):
    # Serve the "Slow and Faithful" page content directly at the homepage
    page = get_object_or_404(Page, slug='well-scripted-life-by-greg-dyche', is_published=True)
    return render(request, 'blog/page_detail.html', {'page': page})

# This function must also be defined to be used below
def debug_view(request):
    db_host = settings.DATABASES['default'].get('HOST', 'Not Found')
    output = f"<h1>Debug Information</h1>"
    output += f"<p><b>Database Host the web app is connected to:</b> {db_host}</p>"
    
    output += "<hr><h2>Session Write Test</h2>"
    try:
        request.session['debug_test'] = 'value_was_set'
        request.session.save()
        output += "<p style='color:green;'><b>Session Write Test: ✅ SUCCESS</b></p>"
        output += "<p>The application successfully wrote a value to the session table.</p>"
    except Exception as e:
        output += f"<p style='color:red;'><b>Session Write Test: ❌ FAILED</b></p>"
        output += f"<p><b>This is the root cause of the login issue.</b></p>"
        output += f"<p><b>Error returned:</b> {e}</p>"
        
    return HttpResponse(output)


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('debug-view/', debug_view, name='debug_view'),
    path('blog/', include('blog.urls', namespace='blog')),
]