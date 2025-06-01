# blog/admin.py
from django.contrib import admin
from .models import Post, Page, Category, Tag, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_date', 'published_date']
    list_filter = ['status', 'created_date', 'categories']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories', 'tags']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'created_date']
    list_filter = ['is_published', 'created_date']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

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