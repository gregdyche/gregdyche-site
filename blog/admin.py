# blog/admin.py
from django.contrib import admin
from .models import Post, Page, PageCategory, Category, Tag, Comment, Subscriber

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_date', 'published_date']
    list_filter = ['status', 'created_date', 'categories']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories', 'tags']

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