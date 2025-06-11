# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based personal blog/website for Greg Dyche, migrated from WordPress. The application is deployed on Railway with PostgreSQL in production and SQLite for local development.

## Architecture

**Tech Stack:**
- Django 5.2.1 with Python 3.12.3
- Database: PostgreSQL (production) / SQLite (development)
- Static files: WhiteNoise for serving
- Deployment: Railway platform
- Frontend: HTML templates with modern CSS styling

**Application Structure:**
- `gregdyche/` - Main Django project configuration
- `blog/` - Blog application containing models, views, templates
- `core/` - Additional Django app (minimal usage)
- WordPress import capability via management commands

**Key Models:**
- `Post` - Blog posts with categories, tags, comments
- `Page` - Static pages (like About, Contact)
- `Category` - Post categorization
- `Tag` - Post tagging
- `Comment` - WordPress-imported comments

## Development Commands

**Local Development:**
```bash
# Start development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser
```

**WordPress Import:**
```bash
# Import WordPress XML export
python manage.py import_wordpress path/to/wordpress_export.xml

# Fix WordPress wp-content URLs to use static files
python manage.py fix_wordpress_links
```

**Testing:**
No specific test framework configured - uses Django's built-in testing.

## Configuration

**Environment Variables:**
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (default: False)
- `DATABASE_URL` - Database connection string
- `ALLOWED_HOSTS` - Comma-separated allowed hosts
- `RAILWAY_STATIC_URL` - Railway deployment URL
- `CUSTOM_DOMAIN` - Custom domain if configured

**Important Settings:**
- Homepage redirects to 'well-scripted-life-by-greg-dyche' page
- CSRF trusted origins configured for Railway deployment
- WhiteNoise handles static file serving
- Time zone: America/Chicago

## Deployment

**Railway Deployment:**
- Uses `Procfile` for process definition
- Automatic migration and static file collection on deploy
- Gunicorn WSGI server
- Environment-based configuration with python-decouple

**Static Files:**
- Development: served from `static/` directory
- Production: collected to `staticfiles/` and served via WhiteNoise
- Media uploads stored in `static/uploads/` directory structure

## WordPress Migration Context

This site was migrated from WordPress, retaining:
- Original post/page content and structure
- Categories and tags
- Comments
- Upload file paths (wp-content URLs converted to static file URLs)
- Original WordPress IDs for reference (`wp_post_id`, `wp_page_id`, `wp_comment_id`)