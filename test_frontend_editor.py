#!/usr/bin/env python
"""
Simple test script to verify the frontend editing system is working
"""
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gregdyche.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Page

def test_editing_system():
    print("Testing Frontend Editing System")
    print("=" * 40)
    
    # Check if server is running
    try:
        response = requests.get('http://localhost:8000/')
        print(f"✓ Django server is running (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("✗ Django server is not running")
        return False
    
    # Check models
    posts = Post.objects.all()
    pages = Page.objects.all()
    print(f"✓ Found {posts.count()} posts and {pages.count()} pages")
    
    # Check staff user exists
    staff_users = User.objects.filter(is_staff=True)
    print(f"✓ Found {staff_users.count()} staff user(s)")
    
    # Test post editing endpoint (without authentication for now)
    if posts.exists():
        test_post = posts.first()
        print(f"✓ Testing with post: '{test_post.title}' (ID: {test_post.id})")
        
        # Note: This will fail due to authentication, but we can check if endpoint exists
        try:
            response = requests.post(
                f'http://localhost:8000/blog/edit/post/{test_post.id}/',
                json={'title': 'Test Title Update'},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 403:
                print("✓ Edit endpoint exists (authentication required as expected)")
            elif response.status_code == 200:
                print("✓ Edit endpoint working")
            else:
                print(f"? Edit endpoint returned status {response.status_code}")
                
        except Exception as e:
            print(f"✗ Error testing edit endpoint: {e}")
    
    # Check static files are collected
    import os
    js_path = 'staticfiles/blog/js/frontend-editor.js'
    css_path = 'staticfiles/blog/css/frontend-editor.css'
    
    if os.path.exists(js_path):
        print("✓ Frontend editor JavaScript is collected")
    else:
        print("✗ Frontend editor JavaScript not found")
        
    if os.path.exists(css_path):
        print("✓ Frontend editor CSS is collected")
    else:
        print("✗ Frontend editor CSS not found")
    
    print("\n" + "=" * 40)
    print("Frontend editing system setup complete!")
    print("\nTo use the system:")
    print("1. Log in as a staff user at /admin/")
    print("2. Visit any blog post or page")
    print("3. Click 'Edit Mode' in the floating toolbar")
    print("4. Click on content to edit inline")
    print("5. Use Ctrl+S to save or Esc to cancel")
    
    return True

if __name__ == '__main__':
    test_editing_system()