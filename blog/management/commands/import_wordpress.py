# Create this file: blog/management/commands/import_wordpress.py

import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils.text import slugify
from blog.models import Post, Page, Category, Tag, Comment
from dateutil import parser as date_parser
import re

class Command(BaseCommand):
    help = 'Import WordPress XML export file'

    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str, help='Path to WordPress XML export file')

    def handle(self, *args, **options):
        xml_file = options['xml_file']
        
        self.stdout.write(f'Starting import from {xml_file}...')
        
        # Parse XML
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # WordPress XML uses namespaces
        namespaces = {
            'wp': 'http://wordpress.org/export/1.2/',
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }
        
        # Import categories
        self.import_categories(root, namespaces)
        
        # Import tags
        self.import_tags(root, namespaces)
        
        # Import posts and pages
        self.import_items(root, namespaces)
        
        self.stdout.write(self.style.SUCCESS('Import completed successfully!'))

    def import_categories(self, root, namespaces):
        categories = root.findall('.//wp:category', namespaces)
        for cat in categories:
            name = cat.find('wp:cat_name', namespaces).text
            slug = cat.find('wp:category_nicename', namespaces).text
            description = cat.find('wp:category_description', namespaces)
            description = description.text if description is not None else ''
            
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slug, 'description': description}
            )
            if created:
                self.stdout.write(f'Created category: {name}')

    def import_tags(self, root, namespaces):
        tags = root.findall('.//wp:tag', namespaces)
        for tag in tags:
            name = tag.find('wp:tag_name', namespaces).text
            slug = tag.find('wp:tag_slug', namespaces).text
            
            tag_obj, created = Tag.objects.get_or_create(
                name=name,
                defaults={'slug': slug}
            )
            if created:
                self.stdout.write(f'Created tag: {name}')

    def import_items(self, root, namespaces):
        items = root.findall('.//item')
        
        for item in items:
            # Get basic info
            title = item.find('title').text or 'Untitled'
            content = item.find('content:encoded', namespaces)
            content = content.text if content is not None else ''
            
            # Get WordPress specific data
            post_type = item.find('wp:post_type', namespaces).text
            status = item.find('wp:status', namespaces).text
            post_id = item.find('wp:post_id', namespaces).text
            
            # Get dates
            pub_date = item.find('pubDate').text
            if pub_date:
                pub_date = date_parser.parse(pub_date)
            
            # Get slug
            post_name = item.find('wp:post_name', namespaces)
            slug = post_name.text if post_name is not None else slugify(title)
            
            # Get excerpt
            excerpt_elem = item.find('excerpt:encoded', namespaces)
            excerpt = excerpt_elem.text if excerpt_elem is not None else ''
            
            # Skip attachments and other non-content types
            if post_type in ['attachment', 'nav_menu_item', 'revision']:
                continue
            
            if post_type == 'post':
                self.import_post(item, title, content, status, post_id, pub_date, slug, excerpt, namespaces)
            elif post_type == 'page':
                self.import_page(item, title, content, status, post_id, pub_date, slug, namespaces)

    def import_post(self, item, title, content, status, post_id, pub_date, slug, excerpt, namespaces):
        # Convert WordPress status to Django choices
        django_status = 'published' if status == 'publish' else 'draft'
        
        post, created = Post.objects.get_or_create(
            wp_post_id=int(post_id),
            defaults={
                'title': title,
                'slug': slug,
                'content': content,
                'excerpt': excerpt,
                'status': django_status,
                'created_date': pub_date,
                'published_date': pub_date if django_status == 'published' else None,
            }
        )
        
        if created:
            # Add categories
            categories = item.findall('.//category[@domain="category"]')
            for cat in categories:
                cat_name = cat.text
                try:
                    category = Category.objects.get(name=cat_name)
                    post.categories.add(category)
                except Category.DoesNotExist:
                    pass
            
            # Add tags
            tags = item.findall('.//category[@domain="post_tag"]')
            for tag in tags:
                tag_name = tag.text
                try:
                    tag_obj = Tag.objects.get(name=tag_name)
                    post.tags.add(tag_obj)
                except Tag.DoesNotExist:
                    pass
            
            self.stdout.write(f'Created post: {title}')
            
            # Import comments
            self.import_comments(item, post, namespaces)

    def import_page(self, item, title, content, status, post_id, pub_date, slug, namespaces):
        is_published = status == 'publish'
        
        page, created = Page.objects.get_or_create(
            wp_page_id=int(post_id),
            defaults={
                'title': title,
                'slug': slug,
                'content': content,
                'is_published': is_published,
                'created_date': pub_date,
            }
        )
        
        if created:
            self.stdout.write(f'Created page: {title}')

    def import_comments(self, item, post, namespaces):
        comments = item.findall('.//wp:comment', namespaces)
        
        for comment in comments:
            comment_id = comment.find('wp:comment_id', namespaces).text
            author = comment.find('wp:comment_author', namespaces).text or 'Anonymous'
            email = comment.find('wp:comment_author_email', namespaces).text or ''
            url = comment.find('wp:comment_author_url', namespaces).text or ''
            date = comment.find('wp:comment_date', namespaces).text
            content = comment.find('wp:comment_content', namespaces).text or ''
            approved = comment.find('wp:comment_approved', namespaces).text == '1'
            
            if date:
                date = date_parser.parse(date)
            
            Comment.objects.get_or_create(
                wp_comment_id=int(comment_id),
                defaults={
                    'post': post,
                    'author_name': author,
                    'author_email': email,
                    'author_url': url,
                    'content': content,
                    'created_date': date,
                    'is_approved': approved,
                }
            )