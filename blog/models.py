from django.db import models

# Create your models here.
# blog/models.py - Replace your entire file with this content

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('private', 'Private'),
    ]
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text="Brief description of the post")
    
    # WordPress import fields
    wp_post_id = models.IntegerField(null=True, blank=True, help_text="Original WordPress post ID")
    
    # Publishing info
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    # Relationships
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    # SEO and social
    meta_description = models.CharField(max_length=160, blank=True)
    featured_image = models.URLField(blank=True, help_text="URL to featured image")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_date', '-created_date']

class Page(models.Model):
    """Static pages like About, Contact, etc."""
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = models.TextField()
    
    # WordPress import fields
    wp_page_id = models.IntegerField(null=True, blank=True)
    
    # Publishing info
    is_published = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:page_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    """Comments from WordPress import"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField(blank=True)
    author_url = models.URLField(blank=True)
    content = models.TextField()
    created_date = models.DateTimeField()
    is_approved = models.BooleanField(default=True)
    
    # WordPress import field
    wp_comment_id = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f'Comment by {self.author_name} on {self.post.title}'
    
    class Meta:
        ordering = ['created_date']