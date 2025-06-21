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

class PageCategory(models.Model):
    """Categories for organizing pages in TOC"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Order in TOC (lower = first)")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Page Categories"

class Page(models.Model):
    """Static pages like About, Contact, etc."""
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = models.TextField()
    
    # TOC organization
    category = models.ForeignKey(PageCategory, on_delete=models.SET_NULL, null=True, blank=True, 
                                help_text="Category for TOC organization")
    toc_order = models.IntegerField(default=0, help_text="Order within category (lower = first)")
    show_in_toc = models.BooleanField(default=True, help_text="Show this page in the TOC")
    
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
    
    class Meta:
        ordering = ['category__order', 'toc_order', 'title']

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

class Subscriber(models.Model):
    """Email subscribers for blog notifications"""
    email = models.EmailField(unique=True, help_text="Subscriber's email address")
    
    # Subscription preferences for different blog categories
    tech = models.BooleanField(default=False, help_text="Subscribe to Technology blog posts")
    life = models.BooleanField(default=False, help_text="Subscribe to Life Management blog posts")
    spirit = models.BooleanField(default=False, help_text="Subscribe to Spiritual Growth blog posts")
    
    # Subscription metadata
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Whether subscription is active")
    confirmation_token = models.CharField(max_length=100, blank=True, help_text="Token for email confirmation")
    confirmed_at = models.DateTimeField(null=True, blank=True, help_text="When email was confirmed")
    
    def __str__(self):
        categories = []
        if self.tech:
            categories.append('Tech')
        if self.life:
            categories.append('Life')
        if self.spirit:
            categories.append('Spirit')
        return f'{self.email} ({", ".join(categories) if categories else "No categories"})'
    
    @property
    def subscribed_categories(self):
        """Return list of subscribed category names"""
        categories = []
        if self.tech:
            categories.append('tech')
        if self.life:
            categories.append('life')
        if self.spirit:
            categories.append('spirit')
        return categories
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"