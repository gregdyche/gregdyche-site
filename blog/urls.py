# blog/urls.py

from django.urls import path
from .views import (
    PostDetailView, PageDetailView, BlogSectionView,
    subscribe_view, subscribe_success_view, unsubscribe_view, unsubscribe_success_view
)

app_name = 'blog'

urlpatterns = [
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
    path('subscribe/', subscribe_view, name='subscribe'),
    path('subscribe/success/', subscribe_success_view, name='subscribe_success'),
    path('unsubscribe/', unsubscribe_view, name='unsubscribe'),
    path('unsubscribe/success/', unsubscribe_success_view, name='unsubscribe_success'),
    path('<str:section>/', BlogSectionView.as_view(), name='blog_section'),
]