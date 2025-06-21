from django.db.models.signals import post_save
from django.dispatch import receiver
from django.test import RequestFactory
from .models import Post
from .utils import send_post_notifications
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Post)
def send_post_notification_on_publish(sender, instance, created, **kwargs):
    """
    Send email notifications to subscribers when a post is published.
    
    This signal is triggered when:
    - A new post is created with status 'published'
    - An existing post's status changes to 'published'
    """
    
    # Only send notifications for published posts
    if instance.status != 'published':
        return
    
    # For new posts, send notifications immediately
    if created:
        logger.info(f'New post created and published: "{instance.title}", sending notifications')
        send_notifications_for_post(instance)
        return
    
    # For existing posts, we'll send notifications on any update to a published post
    # This is simpler and ensures notifications are sent when needed
    # You can manually control this via the admin action if needed
    logger.info(f'Published post updated: "{instance.title}", sending notifications')
    send_notifications_for_post(instance)

def send_notifications_for_post(post):
    """
    Helper function to send notifications for a post.
    Creates a mock request since signals don't have access to the original request.
    """
    try:
        # Create a mock request for the email function
        factory = RequestFactory()
        request = factory.get('/')
        
        # Send notifications
        results = send_post_notifications(request, post)
        
        logger.info(f'Post notification results for "{post.title}": '
                   f'{results["success_count"]} sent, {results["failure_count"]} failed')
        
        if results['errors']:
            for error in results['errors']:
                logger.error(f'Post notification error: {error}')
                
    except Exception as e:
        logger.error(f'Failed to send notifications for post "{post.title}": {str(e)}')

# Alternative approach: Manual notification function for admin use
def manually_send_post_notifications(post):
    """
    Manually send notifications for a post.
    This can be called from Django admin or management commands.
    """
    send_notifications_for_post(post)