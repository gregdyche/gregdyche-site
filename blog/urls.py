# blog/urls.py

from django.urls import path
from .views import (
    PostDetailView, PageDetailView, BlogSectionView,
    subscribe_view, subscribe_success_view, unsubscribe_view, unsubscribe_success_view,
    edit_post_content, edit_page_content
)

app_name = 'blog'

urlpatterns = [
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
    path('subscribe/', subscribe_view, name='subscribe'),
    path('subscribe/success/', subscribe_success_view, name='subscribe_success'),
    path('unsubscribe/', unsubscribe_view, name='unsubscribe'),
    path('unsubscribe/success/', unsubscribe_success_view, name='unsubscribe_success'),
    # Frontend editing endpoints
    path('edit/post/<int:post_id>/', edit_post_content, name='edit_post_content'),
    path('edit/page/<int:page_id>/', edit_page_content, name='edit_page_content'),
    path('<str:section>/', BlogSectionView.as_view(), name='blog_section'),
]