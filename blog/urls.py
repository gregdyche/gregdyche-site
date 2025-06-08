# blog/urls.py

from django.urls import path
from .views import PostDetailView, PageDetailView

app_name = 'blog'

urlpatterns = [
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
]