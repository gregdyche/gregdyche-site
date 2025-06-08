# blog/views.py

from django.views.generic import DetailView
from .models import Post, Page

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    queryset = Post.objects.filter(status='published')

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/page_detail.html'
    queryset = Page.objects.filter(is_published=True)