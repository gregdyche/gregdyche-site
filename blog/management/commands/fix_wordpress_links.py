import re
import os
import requests
from urllib.parse import urlparse
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from blog.models import Post, Page


class Command(BaseCommand):
    help = 'Fix WordPress wp-content links by downloading files and updating URLs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making changes',
        )
        parser.add_argument(
            '--download',
            action='store_true',
            help='Download files from WordPress URLs',
        )

    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.download_files = options['download']
        
        # Patterns to match WordPress wp-content URLs
        patterns = [
            r'https?://gregdyche\.com/wp-content/uploads/([0-9]{4}/[0-9]{2}/[^?\s"\']+)',
            r'https?://gregdychecom\.wordpress\.com/wp-content/uploads/([0-9]{4}/[0-9]{2}/[^?\s"\']+)',
        ]
        
        self.stdout.write(self.style.SUCCESS('Starting WordPress link fix...'))
        
        # Process Posts
        posts = Post.objects.all()
        self.stdout.write(f'Checking {posts.count()} posts...')
        
        for post in posts:
            original_content = post.content
            updated_content = self.fix_content_links(original_content, patterns)
            
            if original_content != updated_content:
                self.stdout.write(f'Post "{post.title}" (ID: {post.id}) has links to fix')
                if not self.dry_run:
                    post.content = updated_content
                    post.save()
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Updated post "{post.title}"'))
                else:
                    self.stdout.write(f'  [DRY RUN] Would update post "{post.title}"')
        
        # Process Pages
        pages = Page.objects.all()
        self.stdout.write(f'Checking {pages.count()} pages...')
        
        for page in pages:
            original_content = page.content
            updated_content = self.fix_content_links(original_content, patterns)
            
            if original_content != updated_content:
                self.stdout.write(f'Page "{page.title}" (ID: {page.id}) has links to fix')
                if not self.dry_run:
                    page.content = updated_content
                    page.save()
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Updated page "{page.title}"'))
                else:
                    self.stdout.write(f'  [DRY RUN] Would update page "{page.title}"')
        
        self.stdout.write(self.style.SUCCESS('WordPress link fix complete!'))

    def fix_content_links(self, content, patterns):
        """Fix WordPress wp-content links in content"""
        updated_content = content
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            
            for match in matches:
                original_url = match.group(0)
                file_path = match.group(1)  # e.g., "2024/03/filename.png"
                
                # Extract filename
                filename = os.path.basename(file_path)
                
                # Create new static URL
                new_url = f'/static/uploads/{file_path}'
                
                self.stdout.write(f'  Found: {original_url}')
                self.stdout.write(f'  Will become: {new_url}')
                
                # Download file if requested
                if self.download_files:
                    self.download_file(original_url, file_path)
                
                # Replace the URL in content
                updated_content = updated_content.replace(original_url, new_url)
        
        return updated_content

    def download_file(self, url, file_path):
        """Download a file from WordPress to the static directory"""
        try:
            # Create the full local path
            local_dir = settings.BASE_DIR / 'static' / 'uploads' / os.path.dirname(file_path)
            local_dir.mkdir(parents=True, exist_ok=True)
            
            local_file_path = settings.BASE_DIR / 'static' / 'uploads' / file_path
            
            # Skip if file already exists
            if local_file_path.exists():
                self.stdout.write(f'    File already exists: {local_file_path}')
                return
            
            # Download the file
            self.stdout.write(f'    Downloading: {url}')
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save the file
            with open(local_file_path, 'wb') as f:
                f.write(response.content)
            
            self.stdout.write(self.style.SUCCESS(f'    ✓ Downloaded: {local_file_path}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'    ✗ Failed to download {url}: {e}'))