# gregdyche/urls.py

from django.contrib import admin
from django.urls import path, include  # <-- Make sure to import 'include'
from django.http import HttpResponse
from django.conf import settings

# ... (your home and debug_view functions) ...

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('debug-view/', debug_view, name='debug_view'),
    
    # --- ADD THIS LINE ---
    path('blog/', include('blog.urls', namespace='blog')),
]