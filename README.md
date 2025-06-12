# Greg Dyche Personal Website

A Django-based personal blog/website migrated from WordPress, deployed on Railway.

## Quick Start

1. **Navigate to project directory:**
   ```bash
   cd gregdyche_site
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the site:**
   - Website: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Tech Stack

- Django 5.2.1 with Python 3.12.3
- Database: PostgreSQL (production) / SQLite (development)
- Deployment: Railway platform
- Static files: WhiteNoise

## Key Commands

```bash
# Create superuser for admin access
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Make database migrations
python manage.py makemigrations

# WordPress import (if needed)
python manage.py import_wordpress path/to/export.xml
python manage.py fix_wordpress_links
```

## Environment Setup

Create a `.env` file with:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

## Deployment

Deployed on Railway with automatic deployments from the main branch.
