"""
URL configuration for gregdyche project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Greg. This is your Railway app.")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
]