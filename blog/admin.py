# blog/admin.py
from django.contrib import admin
from django.test import RequestFactory
from .models import Post, Page, PageCategory, Category, Tag, Comment, Subscriber
from .utils import send_post_notifications

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_date', 'published_date']
    list_filter = ['status', 'created_date', 'categories']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories', 'tags']
    actions = ['send_post_notifications_action']
    
    def send_post_notifications_action(self, request, queryset):
        """Admin action to manually send post notifications"""
        total_sent = 0
        total_failed = 0
        
        for post in queryset:
            if post.status != 'published':
                self.message_user(request, f'Skipped "{post.title}" - not published', level='warning')
                continue
                
            # Create a mock request for the email function
            factory = RequestFactory()
            mock_request = factory.get('/')
            
            # Send notifications
            results = send_post_notifications(mock_request, post)
            total_sent += results['success_count']
            total_failed += results['failure_count']
            
            if results['success_count'] > 0:
                self.message_user(
                    request, 
                    f'Sent {results["success_count"]} notifications for "{post.title}"'
                )
            
            if results['failure_count'] > 0:
                self.message_user(
                    request, 
                    f'Failed to send {results["failure_count"]} notifications for "{post.title}"',
                    level='error'
                )
        
        if total_sent > 0 or total_failed > 0:
            self.message_user(
                request, 
                f'Notification summary: {total_sent} sent, {total_failed} failed'
            )
    
    send_post_notifications_action.short_description = "Send email notifications to subscribers"

@admin.register(PageCategory)
class PageCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'toc_order', 'show_in_toc', 'is_published', 'created_date']
    list_filter = ['category', 'show_in_toc', 'is_published', 'created_date']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['toc_order', 'show_in_toc']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'created_date', 'is_approved']
    list_filter = ['is_approved', 'created_date']
    search_fields = ['author_name', 'content']

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'tech', 'life', 'spirit', 'is_active', 'subscribed_at']
    list_filter = ['tech', 'life', 'spirit', 'is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at', 'confirmation_token', 'confirmed_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'is_active')
        }),
        ('Subscription Preferences', {
            'fields': ('tech', 'life', 'spirit'),
            'description': 'Select which blog categories this subscriber wants to receive notifications for.'
        }),
        ('Metadata', {
            'fields': ('subscribed_at', 'confirmation_token', 'confirmed_at'),
            'classes': ('collapse',),
            'description': 'System-generated information about the subscription.'
        }),
    )
    
    def get_queryset(self, request):
        """Override to show most recent subscribers first"""
        return super().get_queryset(request).order_by('-subscribed_at')
    
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        """Action to activate selected subscribers"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscribers were successfully activated.')
    activate_subscribers.short_description = "Activate selected subscribers"
    
    def deactivate_subscribers(self, request, queryset):
        """Action to deactivate selected subscribers"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscribers were successfully deactivated.')
    deactivate_subscribers.short_description = "Deactivate selected subscribers"