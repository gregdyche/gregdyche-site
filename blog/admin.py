# blog/admin.py
from django.contrib import admin
from django.test import RequestFactory
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Post, Page, PageCategory, Category, Tag, Comment, Subscriber
from .utils import send_post_notifications

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured_image_thumbnail', 'status', 'created_date', 'published_date']
    list_filter = ['status', 'created_date', 'categories']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories', 'tags']
    actions = ['send_post_notifications_action']
    
    # Organize fields into logical sections
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt')
        }),
        ('Images', {
            'fields': ('featured_image_upload', 'featured_image_preview', 'thumbnail_image', 'thumbnail_preview', 'banner_image', 'banner_preview', 'featured_image'),
            'description': 'Upload images for this post. Featured image upload is recommended over URL.'
        }),
        ('Publishing', {
            'fields': ('status', 'published_date')
        }),
        ('Categorization', {
            'fields': ('categories', 'tags'),
            'classes': ('wide',)
        }),
        ('SEO & Meta', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('WordPress Import Data', {
            'fields': ('wp_post_id',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['featured_image_preview', 'thumbnail_preview', 'banner_preview']
    
    def featured_image_thumbnail(self, obj):
        """Display small thumbnail in list view"""
        if obj.get_featured_image_url():
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.get_featured_image_url()
            )
        return "No image"
    featured_image_thumbnail.short_description = "Image"
    
    def featured_image_preview(self, obj):
        """Display larger preview in edit form"""
        if obj.featured_image_upload:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 8px;" />',
                obj.featured_image_upload.url
            )
        return "No featured image uploaded"
    featured_image_preview.short_description = "Featured Image Preview"
    
    def thumbnail_preview(self, obj):
        """Display thumbnail preview"""
        if obj.thumbnail_image:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 100px; object-fit: cover; border-radius: 8px;" />',
                obj.thumbnail_image.url
            )
        return "No thumbnail uploaded"
    thumbnail_preview.short_description = "Thumbnail Preview"
    
    def banner_preview(self, obj):
        """Display banner preview"""
        if obj.banner_image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 150px; object-fit: cover; border-radius: 8px;" />',
                obj.banner_image.url
            )
        return "No banner uploaded"
    banner_preview.short_description = "Banner Preview"
    
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
    list_display = ['title', 'featured_image_thumbnail', 'category', 'toc_order', 'show_in_toc', 'is_published', 'created_date']
    list_filter = ['category', 'show_in_toc', 'is_published', 'created_date']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['toc_order', 'show_in_toc']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content')
        }),
        ('Images', {
            'fields': ('featured_image', 'featured_image_preview', 'banner_image', 'banner_preview'),
            'description': 'Upload images for this page.'
        }),
        ('Table of Contents', {
            'fields': ('category', 'toc_order', 'show_in_toc'),
            'description': 'Controls how this page appears in the site navigation.'
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('SEO & Meta', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('WordPress Import Data', {
            'fields': ('wp_page_id',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['featured_image_preview', 'banner_preview']
    
    def featured_image_thumbnail(self, obj):
        """Display small thumbnail in list view"""
        if obj.get_featured_image_url():
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.get_featured_image_url()
            )
        return "No image"
    featured_image_thumbnail.short_description = "Image"
    
    def featured_image_preview(self, obj):
        """Display featured image preview"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; border-radius: 8px;" />',
                obj.featured_image.url
            )
        return "No featured image uploaded"
    featured_image_preview.short_description = "Featured Image Preview"
    
    def banner_preview(self, obj):
        """Display banner preview"""
        if obj.banner_image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 150px; object-fit: cover; border-radius: 8px;" />',
                obj.banner_image.url
            )
        return "No banner uploaded"
    banner_preview.short_description = "Banner Preview"

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