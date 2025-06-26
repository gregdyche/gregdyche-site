# blog/views.py

from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Post, Page, Category, Subscriber
from .forms import SubscriptionForm, CoachingInquiryForm, ContactPageInquiryForm
from .utils import send_subscription_notification, send_welcome_email

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
                
                # Send notification email to admin
                notification_sent = send_subscription_notification(request, subscriber)
                
                # Send welcome email to subscriber (optional)
                welcome_sent = send_welcome_email(request, subscriber)
                
                # Log email status (for debugging)
                if not notification_sent:
                    print(f"Warning: Failed to send notification email for {subscriber.email}")
                if not welcome_sent:
                    print(f"Warning: Failed to send welcome email to {subscriber.email}")
                
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

# Frontend Editing Views
def is_staff_user(user):
    """Check if user is staff member"""
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff_user)
@require_POST
@csrf_exempt
def edit_post_content(request, post_id):
    """AJAX endpoint to update post content"""
    try:
        post = get_object_or_404(Post, id=post_id)
        data = json.loads(request.body)
        
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        if 'excerpt' in data:
            post.excerpt = data['excerpt']
            
        post.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Post updated successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@user_passes_test(is_staff_user)
@require_POST  
@csrf_exempt
def edit_page_content(request, page_id):
    """AJAX endpoint to update page content"""
    try:
        page = get_object_or_404(Page, id=page_id)
        data = json.loads(request.body)
        
        if 'title' in data:
            page.title = data['title']
        if 'content' in data:
            page.content = data['content']
            
        page.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Page updated successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


def coaching_inquiry(request):
    """Handle coaching and contact form submissions"""
    referer = request.META.get('HTTP_REFERER', '')
    is_contact_page_submission = 'contact' in referer

    if request.method == 'POST':
        if is_contact_page_submission:
            form = ContactPageInquiryForm(request.POST)
            form_source = 'contact form'
            success_redirect_url = '/blog/page/contact/'
            interest_choices = dict(ContactPageInquiryForm.INTEREST_CHOICES)
        else:
            form = CoachingInquiryForm(request.POST)
            form_source = 'coaching form'
            success_redirect_url = '/blog/page/coaching/'
            interest_choices = dict(CoachingInquiryForm.INTEREST_CHOICES)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            interest_key = form.cleaned_data['interest']
            message_content = form.cleaned_data['message']
            
            interest_display = interest_choices.get(interest_key, interest_key) # Get display name

            from django.core.mail import send_mail
            from django.conf import settings
            import requests # For Google Chat
            import json     # For Google Chat
            
            subject = f'New {form_source} message from {name}'
            
            email_body = f"""
New {form_source} submission received:

Name: {name}
Email: {email}
Interest: {interest_display}

Message:
{message_content}

---
Sent from Well Scripted Life {form_source} (Referer: {referer})
"""
            
            try:
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL_RECIPIENT if hasattr(settings, 'ADMIN_EMAIL_RECIPIENT') else 'gregdyche@gmail.com'], # Use setting or fallback
                    fail_silently=False,
                )
                messages.success(request, 'Thank you! Your message has been sent. I\'ll get back to you soon.')
                
                # Send Google Chat notification
                google_chat_webhook_url = getattr(settings, 'GOOGLE_CHAT_WEBHOOK_URL', None)
                if google_chat_webhook_url:
                    chat_message_text = f"🔔 *New {form_source} submission received!*\n\n*Name:* {name}\n*Email:* {email}\n*Interest:* {interest_display}\n*Message:*\n```{message_content}```\n\nRaw Referer: {referer}"
                    google_chat_payload = {'text': chat_message_text}
                    try:
                        response = requests.post(
                            google_chat_webhook_url,
                            headers={'Content-Type': 'application/json; charset=UTF-8'},
                            data=json.dumps(google_chat_payload),
                            timeout=5 # Add a timeout
                        )
                        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                        print(f"Successfully sent message to Google Chat for {form_source} from {name}")
                    except requests.exceptions.Timeout:
                        print(f"Error sending message to Google Chat: Timeout for {form_source} from {name}")
                    except requests.exceptions.RequestException as chat_e:
                        print(f"Error sending message to Google Chat for {form_source} from {name}: {chat_e}")
                    except Exception as general_chat_e:
                        print(f"An unexpected error occurred while sending to Google Chat for {form_source} from {name}: {general_chat_e}")
                else:
                    print("GOOGLE_CHAT_WEBHOOK_URL not configured. Skipping Google Chat notification.")

            except Exception as e:
                messages.error(request, f'There was an error sending your message: {e}. Please try emailing me directly.')
            
            return redirect(success_redirect_url)
        else:
            # Form is not valid, add errors to messages and redirect back to the original page
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect(referer if referer else ('/blog/page/contact/' if is_contact_page_submission else '/blog/page/coaching/'))
    else:
        # For GET requests, redirect to the appropriate page (though ideally, forms are on their own pages or handled by page view)
        return redirect('/blog/page/contact/' if is_contact_page_submission else '/blog/page/coaching/')