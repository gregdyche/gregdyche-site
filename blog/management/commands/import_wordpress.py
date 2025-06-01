# blog/management/commands/import_wordpress.py
# Most robust version - handles all edge cases

import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils.text import slugify
from django.utils import timezone
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

    def get_unique_slug(self, base_slug, model_class):
        """Generate a unique slug by appending numbers if needed"""
        if not base_slug:
            base_slug = 'untitled'
        
        slug = base_slug
        counter = 1
        
        while model_class.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        return slug

    def import_categories(self, root, namespaces):
        categories = root.findall('.//wp:category', namespaces)
        for cat in categories:
            name_elem = cat.find('wp:cat_name', namespaces)
            if name_elem is None or not name_elem.text:
                continue
                
            name = name_elem.text
            slug_elem = cat.find('wp:category_nicename', namespaces)
            slug = slug_elem.text if slug_elem is not None else slugify(name)
            
            description_elem = cat.find('wp:category_description', namespaces)
            description = description_elem.text if description_elem is not None else ''
            
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': self.get_unique_slug(slug, Category), 'description': description}
            )
            if created:
                self.stdout.write(f'Created category: {name}')

    def import_tags(self, root, namespaces):
        tags = root.findall('.//wp:tag', namespaces)
        for tag in tags:
            name_elem = tag.find('wp:tag_name', namespaces)
            if name_elem is None or not name_elem.text:
                continue
                
            name = name_elem.text
            slug_elem = tag.find('wp:tag_slug', namespaces)
            slug = slug_elem.text if slug_elem is not None else slugify(name)
            
            tag_obj, created = Tag.objects.get_or_create(
                name=name,
                defaults={'slug': self.get_unique_slug(slug, Tag)}
            )
            if created:
                self.stdout.write(f'Created tag: {name}')

    def import_items(self, root, namespaces):
        items = root.findall('.//item')
        
        for item in items:
            try:
                # Get basic info
                title_elem = item.find('title')
                title = title_elem.text if title_elem is not None and title_elem.text else 'Untitled'
                
                content_elem = item.find('content:encoded', namespaces)
                content = content_elem.text if content_elem is not None and content_elem.text else ''
                
                # Get WordPress specific data
                post_type_elem = item.find('wp:post_type', namespaces)
                post_type = post_type_elem.text if post_type_elem is not None else 'post'
                
                status_elem = item.find('wp:status', namespaces)
                status = status_elem.text if status_elem is not None else 'publish'
                
                post_id_elem = item.find('wp:post_id', namespaces)
                post_id = post_id_elem.text if post_id_elem is not None else '0'
                
                # Get dates - handle missing dates gracefully
                pub_date_elem = item.find('pubDate')
                pub_date = None
                
                if pub_date_elem is not None and pub_date_elem.text:
                    try:
                        pub_date = date_parser.parse(pub_date_elem.text)
                    except:
                        pass
                
                if pub_date is None:
                    pub_date = timezone.now()
                
                # Get slug
                post_name_elem = item.find('wp:post_name', namespaces)
                base_slug = post_name_elem.text if post_name_elem is not None and post_name_elem.text else slugify(title)
                
                # Get excerpt
                excerpt_elem = item.find('excerpt:encoded', namespaces)
                excerpt = excerpt_elem.text if excerpt_elem is not None and excerpt_elem.text else ''
                
                # Skip attachments and other non-content types
                if post_type in ['attachment', 'nav_menu_item', 'revision']:
                    continue
                
                # Skip items that already exist
                if post_type == 'post' and Post.objects.filter(wp_post_id=int(post_id)).exists():
                    continue
                elif post_type == 'page' and Page.objects.filter(wp_page_id=int(post_id)).exists():
                    continue
                
                if post_type == 'post':
                    self.import_post(item, title, content, status, post_id, pub_date, base_slug, excerpt, namespaces)
                elif post_type == 'page':
                    self.import_page(item, title, content, status, post_id, pub_date, base_slug, namespaces)
                    
            except Exception as e:
                self.stdout.write(f'Error processing item: {e}')
                continue

    def import_post(self, item, title, content, status, post_id, pub_date, base_slug, excerpt, namespaces):
        try:
            # Convert WordPress status to Django choices
            django_status = 'published' if status == 'publish' else 'draft'
            
            # Get unique slug
            slug = self.get_unique_slug(base_slug, Post)
            
            post = Post.objects.create(
                wp_post_id=int(post_id),
                title=title,
                slug=slug,
                content=content,
                excerpt=excerpt,
                status=django_status,
                created_date=pub_date,
                published_date=pub_date if django_status == 'published' else None,
            )
            
            # Add categories
            categories = item.findall('.//category[@domain="category"]')
            for cat in categories:
                if cat.text:
                    try:
                        category = Category.objects.get(name=cat.text)
                        post.categories.add(category)
                    except Category.DoesNotExist:
                        pass
            
            # Add tags
            tags = item.findall('.//category[@domain="post_tag"]')
            for tag in tags:
                if tag.text:
                    try:
                        tag_obj = Tag.objects.get(name=tag.text)
                        post.tags.add(tag_obj)
                    except Tag.DoesNotExist:
                        pass
            
            self.stdout.write(f'Created post: {title}')
            
            # Import comments
            self.import_comments(item, post, namespaces)
            
        except Exception as e:
            self.stdout.write(f'Error creating post "{title}": {e}')

    def import_page(self, item, title, content, status, post_id, pub_date, base_slug, namespaces):
        try:
            is_published = status == 'publish'
            
            # Get unique slug
            slug = self.get_unique_slug(base_slug, Page)
            
            page = Page.objects.create(
                wp_page_id=int(post_id),
                title=title,
                slug=slug,
                content=content,
                is_published=is_published,
                created_date=pub_date,
            )
            
            self.stdout.write(f'Created page: {title}')
            
        except Exception as e:
            self.stdout.write(f'Error creating page "{title}": {e}')

    def import_comments(self, item, post, namespaces):
        comments = item.findall('.//wp:comment', namespaces)
        
        for comment in comments:
            try:
                comment_id_elem = comment.find('wp:comment_id', namespaces)
                if comment_id_elem is None:
                    continue
                    
                comment_id = comment_id_elem.text
                
                # Skip if comment already exists
                if Comment.objects.filter(wp_comment_id=int(comment_id)).exists():
                    continue
                
                author_elem = comment.find('wp:comment_author', namespaces)
                author = author_elem.text if author_elem is not None and author_elem.text else 'Anonymous'
                
                email_elem = comment.find('wp:comment_author_email', namespaces)
                email = email_elem.text if email_elem is not None and email_elem.text else ''
                
                url_elem = comment.find('wp:comment_author_url', namespaces)
                url = url_elem.text if url_elem is not None and url_elem.text else ''
                
                date_elem = comment.find('wp:comment_date', namespaces)
                date = timezone.now()
                
                if date_elem is not None and date_elem.text:
                    try:
                        date = date_parser.parse(date_elem.text)
                    except:
                        pass
                
                content_elem = comment.find('wp:comment_content', namespaces)
                content = content_elem.text if content_elem is not None and content_elem.text else ''
                
                approved_elem = comment.find('wp:comment_approved', namespaces)
                approved = approved_elem.text == '1' if approved_elem is not None else True
                
                Comment.objects.create(
                    wp_comment_id=int(comment_id),
                    post=post,
                    author_name=author,
                    author_email=email,
                    author_url=url,
                    content=content,
                    created_date=date,
                    is_approved=approved,
                )
                
            except Exception as e:
                self.stdout.write(f'Error creating comment: {e}')
                continue