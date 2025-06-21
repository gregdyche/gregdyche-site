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