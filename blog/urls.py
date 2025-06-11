# blog/urls.py

from django.urls import path
from .views import PostDetailView, PageDetailView, BlogSectionView

app_name = 'blog'

urlpatterns = [
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
    path('<str:section>/', BlogSectionView.as_view(), name='blog_section'),
]