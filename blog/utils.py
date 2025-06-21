from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
import logging

logger = logging.getLogger(__name__)

def send_subscription_notification(request, subscriber):
    """
    Send email notification to admin when someone subscribes to the blog.
    
    Args:
        request: The HTTP request object (for getting domain)
        subscriber: The Subscriber model instance
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get current site domain
        current_site = get_current_site(request)
        domain = current_site.domain
        
        # Email context
        context = {
            'subscriber': subscriber,
            'domain': domain,
        }
        
        # Email subject
        categories = subscriber.subscribed_categories
        category_text = ', '.join([cat.title() for cat in categories])
        subject = f'🎉 New Blog Subscription: {subscriber.email} ({category_text})'
        
        # Recipient email
        to_email = settings.SUBSCRIPTION_NOTIFICATION_EMAIL
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Render email templates
        text_content = render_to_string(
            'blog/emails/new_subscription_notification.txt', 
            context
        )
        html_content = render_to_string(
            'blog/emails/new_subscription_notification.html', 
            context
        )
        
        # Create email message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        msg.attach_alternative(html_content, "text/html")
        
        # Send email
        msg.send()
        
        logger.info(f'Subscription notification sent successfully for {subscriber.email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send subscription notification for {subscriber.email}: {str(e)}')
        return False

def send_welcome_email(request, subscriber):
    """
    Send welcome email to new subscriber.
    
    Args:
        request: The HTTP request object
        subscriber: The Subscriber model instance
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get current site domain
        current_site = get_current_site(request)
        domain = current_site.domain
        
        # Email context
        context = {
            'subscriber': subscriber,
            'domain': domain,
        }
        
        # Email subject
        subject = 'Welcome to Well Scripted Life!'
        
        # Recipient email
        to_email = subscriber.email
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # For now, send a simple welcome message
        # You can create welcome email templates later if needed
        text_content = f"""
Hi there!

Thank you for subscribing to Well Scripted Life!

You've subscribed to receive updates for: {', '.join([cat.title() for cat in subscriber.subscribed_categories])}

You'll receive notifications when new content is published in your selected categories.

Best regards,
Greg Dyche
{domain}

---
To manage your subscription or unsubscribe, visit: https://{domain}/blog/unsubscribe/
"""
        
        # Create email message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        
        # Send email
        msg.send()
        
        logger.info(f'Welcome email sent successfully to {subscriber.email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send welcome email to {subscriber.email}: {str(e)}')
        return False

def send_post_notifications(request, post):
    """
    Send email notifications to subscribers when a new post is published.
    
    Args:
        request: The HTTP request object (for getting domain)
        post: The Post model instance that was published
    
    Returns:
        dict: Results of email sending (success_count, failure_count, errors)
    """
    try:
        # Import here to avoid circular imports
        from .models import Subscriber
        
        # Get current site domain
        current_site = get_current_site(request)
        domain = current_site.domain
        
        # Get post categories
        post_categories = post.categories.all()
        if not post_categories:
            logger.info(f'Post "{post.title}" has no categories, skipping notifications')
            return {'success_count': 0, 'failure_count': 0, 'errors': []}
        
        # Find relevant subscribers based on post categories
        relevant_subscribers = Subscriber.objects.filter(is_active=True)
        
        # Filter subscribers who are interested in at least one of the post's categories
        category_filters = []
        for category in post_categories:
            if category.name.lower() == 'tech':
                category_filters.append('tech')
            elif category.name.lower() == 'life':
                category_filters.append('life')
            elif category.name.lower() == 'spirit':
                category_filters.append('spirit')
        
        if not category_filters:
            logger.info(f'Post "{post.title}" categories do not match subscription categories')
            return {'success_count': 0, 'failure_count': 0, 'errors': []}
        
        # Build Q objects for filtering
        from django.db.models import Q
        filter_q = Q()
        for cat_filter in category_filters:
            filter_q |= Q(**{cat_filter: True})
        
        relevant_subscribers = relevant_subscribers.filter(filter_q)
        
        if not relevant_subscribers.exists():
            logger.info(f'No subscribers found for post "{post.title}" categories')
            return {'success_count': 0, 'failure_count': 0, 'errors': []}
        
        # Email subject
        category_names = [cat.name for cat in post_categories]
        subject = f'📝 New {"/".join(category_names)} Post: {post.title}'
        
        # From email
        from_email = settings.DEFAULT_FROM_EMAIL
        
        success_count = 0
        failure_count = 0
        errors = []
        
        # Send emails to relevant subscribers
        for subscriber in relevant_subscribers:
            try:
                # Email context for this subscriber
                context = {
                    'post': post,
                    'subscriber': subscriber,
                    'domain': domain,
                }
                
                # Render email templates
                text_content = render_to_string(
                    'blog/emails/new_post_notification.txt', 
                    context
                )
                html_content = render_to_string(
                    'blog/emails/new_post_notification.html', 
                    context
                )
                
                # Create email message
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=from_email,
                    to=[subscriber.email]
                )
                msg.attach_alternative(html_content, "text/html")
                
                # Send email
                msg.send()
                success_count += 1
                
                logger.info(f'Post notification sent successfully to {subscriber.email} for post "{post.title}"')
                
            except Exception as e:
                failure_count += 1
                error_msg = f'Failed to send post notification to {subscriber.email}: {str(e)}'
                logger.error(error_msg)
                errors.append(error_msg)
        
        logger.info(f'Post notifications completed for "{post.title}": {success_count} sent, {failure_count} failed')
        
        return {
            'success_count': success_count,
            'failure_count': failure_count,
            'errors': errors
        }
        
    except Exception as e:
        logger.error(f'Failed to send post notifications for "{post.title}": {str(e)}')
        return {
            'success_count': 0,
            'failure_count': 0,
            'errors': [str(e)]
        }