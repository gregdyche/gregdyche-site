# blog/views.py

from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Post, Page, Category, Subscriber
from .forms import SubscriptionForm

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
            queryset = queryset.filter(categories__name='Tech').distinct()
        elif section == 'life':
            queryset = queryset.filter(categories__name='Life').distinct()
        elif section == 'spirit':
            queryset = queryset.filter(categories__name='Spirit').distinct()
        
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

def subscribe_view(request):
    """Handle blog subscription form submission"""
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            try:
                subscriber = form.save()
                messages.success(
                    request, 
                    f'Thank you for subscribing! You\'ll receive notifications for {", ".join([cat.title() for cat in subscriber.subscribed_categories])} blog posts.'
                )
                # If it's an AJAX request, return JSON response
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True, 
                        'message': 'Successfully subscribed!'
                    })
                return redirect('blog:subscribe_success')
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again.')
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False, 
                        'message': 'An error occurred. Please try again.'
                    })
        else:
            # Handle form errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'errors': form.errors,
                    'message': 'Please correct the errors below.'
                })
    else:
        form = SubscriptionForm()
    
    return render(request, 'blog/subscribe.html', {'form': form})

def subscribe_success_view(request):
    """Thank you page after successful subscription"""
    return render(request, 'blog/subscribe_success.html')

def unsubscribe_view(request, email=None):
    """Handle unsubscribe requests"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                subscriber = Subscriber.objects.get(email=email, is_active=True)
                subscriber.is_active = False
                subscriber.save()
                messages.success(request, 'You have been successfully unsubscribed.')
                return redirect('blog:unsubscribe_success')
            except Subscriber.DoesNotExist:
                messages.error(request, 'Email address not found in our subscription list.')
        else:
            messages.error(request, 'Please provide a valid email address.')
    
    return render(request, 'blog/unsubscribe.html')

def unsubscribe_success_view(request):
    """Confirmation page after successful unsubscription"""
    return render(request, 'blog/unsubscribe_success.html')