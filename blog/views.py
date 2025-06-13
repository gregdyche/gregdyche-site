# blog/views.py

from django.views.generic import DetailView, ListView
from django.shortcuts import render
from .models import Post, Page, Category

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    queryset = Post.objects.filter(status='published')

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/page_detail.html'
    queryset = Page.objects.filter(is_published=True)

class BlogSectionView(ListView):
    model = Post
    template_name = 'blog/blog_section.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        section = self.kwargs.get('section')
        queryset = Post.objects.filter(status='published')
        
        # Filter by section based on categories
        if section == 'tech':
            tech_categories = ['Technology', 'Python', 'Programming', 'AI', 'Development', 'Tech Stack']
            queryset = queryset.filter(categories__name__in=tech_categories).distinct()
        elif section == 'life':
            life_categories = ['Life Management', 'Productivity', 'Education', 'Workflows', 'Personal']
            queryset = queryset.filter(categories__name__in=life_categories).distinct()
        elif section == 'spirit':
            spirit_categories = ['Spiritual', 'Faith', 'Philosophy', 'Reflection', 'Growth']
            queryset = queryset.filter(categories__name__in=spirit_categories).distinct()
        
        return queryset.order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = self.kwargs.get('section')
        
        section_info = {
            'tech': {
                'title': 'Technology Blog',
                'subtitle': 'Code, Tools & Innovation',
                'description': 'Python development, AI/ML insights, development workflows, and emerging technologies.'
            },
            'life': {
                'title': 'Life Management Blog',
                'subtitle': 'Systems & Productivity', 
                'description': 'Personal workflows, productivity systems, education insights, and life optimization.'
            },
            'spirit': {
                'title': 'Spiritual Growth Blog',
                'subtitle': 'Faith & Reflection',
                'description': 'Thoughts on faith, intentional living, and finding meaning in daily life.'
            }
        }
        
        context['section'] = section
        context['section_info'] = section_info.get(section, {})
        return context