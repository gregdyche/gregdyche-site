# gregdyche/urls.py

"""
URL configuration for gregdyche project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.conf import settings  # --- ADDED IMPORT ---

# This is your existing home view
def home(request):
    return HttpResponse("Hello, Greg. This is your Railway app.")

# --- ADDED DEBUG VIEW FUNCTION ---
def debug_view(request):
    db_host = settings.DATABASES['default'].get('HOST', 'Not Found')
    output = f"<h1>Debug Information</h1>"
    output += f"<p><b>Database Host the web app is connected to:</b> {db_host}</p>"
    
    output += "<hr><h2>Session Write Test</h2>"
    try:
        # This is the key test: we try to write to the session
        request.session['debug_test'] = 'value_was_set'
        request.session.save()
        output += "<p style='color:green;'><b>Session Write Test: ✅ SUCCESS</b></p>"
        output += "<p>The application successfully wrote a value to the session table.</p>"
    except Exception as e:
        output += f"<p style='color:red;'><b>Session Write Test: ❌ FAILED</b></p>"
        output += f"<p><b>This is the root cause of the login issue.</b></p>"
        output += f"<p><b>Error returned:</b> {e}</p>"
        
    return HttpResponse(output)
# --- END OF ADDED FUNCTION ---


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    
    # --- ADDED DEBUG URL ---
    path('debug-view/', debug_view, name='debug_view'),
]