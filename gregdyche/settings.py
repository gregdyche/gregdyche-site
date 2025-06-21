# gregdyche/settings.py

import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core Security Settings ---

# SECRET_KEY is loaded from the .env file or environment variables.
# IMPORTANT: Keep this key secret in production!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-key-for-local-development')

# DEBUG is set to False in production for security.
# It is loaded from the environment, defaulting to True for local dev.
DEBUG = config('DEBUG', default=False, cast=bool)

# --- Host and Origin Configuration ---

# ALLOWED_HOSTS defines which domains can serve the Django site.
# We start with any custom domains, loaded from an env variable.
# Example: 'www.gregdyche.com,gregdyche.com'
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',') if s.strip()])

# Always add the Railway deployment domain
ALLOWED_HOSTS.extend([
    'site-setup-production.up.railway.app',
    '*.up.railway.app',
])

# Add custom domains if configured
CUSTOM_DOMAIN = config('CUSTOM_DOMAIN', default=None)
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.extend([
        CUSTOM_DOMAIN,
        f'www.{CUSTOM_DOMAIN}',
    ])

# In production on Railway, we add the service domains automatically.
if not DEBUG:
    RAILWAY_URL = config('RAILWAY_STATIC_URL', default=None)
    if RAILWAY_URL:
        # The RAILWAY_STATIC_URL might be in format "https://domain" or just "domain"
        if '//' in RAILWAY_URL:
            RAILWAY_HOSTNAME = RAILWAY_URL.split('//')[1]
        else:
            RAILWAY_HOSTNAME = RAILWAY_URL
        if RAILWAY_HOSTNAME not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(RAILWAY_HOSTNAME)

# CSRF_TRUSTED_ORIGINS must include the URLs that will be making POST requests.
# This is crucial for the login form to work in production.
CSRF_TRUSTED_ORIGINS = [
    'https://site-setup-production.up.railway.app'
]

# Add custom domain to CSRF trusted origins if configured
if CUSTOM_DOMAIN:
    CSRF_TRUSTED_ORIGINS.extend([
        f"https://{CUSTOM_DOMAIN}",
        f"https://www.{CUSTOM_DOMAIN}",
    ])



# --- Application Definition ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'blog.apps.BlogConfig',
]

# Required for django.contrib.sites
SITE_ID = 1

MIDDLEWARE = [
    # SecurityMiddleware should be near the top.
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise serves static files efficiently in production.
    # It should be placed directly after SecurityMiddleware.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gregdyche.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'blog/templates')], # Add this line
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.toc_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'gregdyche.wsgi.application'

# --- Database Configuration ---

# --- Database Configuration ---

# This new configuration ensures python-decouple reads the .env file first.
DATABASE_URL = config('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# --- Password Validation ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_TZ = True

# --- Static & Media Files ---

# URL to use when referring to static files.
STATIC_URL = '/static/'
# The absolute path to the directory where collectstatic will gather static files.
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Additional directories for static files (for development)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# Tell Django to use WhiteNoise for serving static files in production.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# URL for user-uploaded media files.
MEDIA_URL = '/media/'
# Directory for storing user-uploaded media files.
# Note: This is not suitable for production on ephemeral filesystems like Railway.
# Consider using a service like AWS S3 for production media storage.
MEDIA_ROOT = BASE_DIR / 'media'


# --- Default Primary Key ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Production Security Settings (Proxy Configuration) ---
# These are critical for running behind a reverse proxy like Railway's.

if not DEBUG:
    # Tell Django to trust the 'X-Forwarded-Proto' header from the proxy.
    # This is essential for recognizing HTTPS connections and for CSRF to work.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Enforce that session and CSRF cookies are only sent over HTTPS.
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # It's also a good practice to enable HSTS (HTTP Strict Transport Security)
    # SECURE_HSTS_SECONDS = 31536000 # 1 year
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True

# --- Email Configuration ---

# Use console backend for development and testing (emails will be printed to console)
# In production, configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD via environment variables
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
if DEBUG or not EMAIL_HOST_USER:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Production email settings (configured via environment variables)
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

# Default email addresses
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@gregdyche.com')
ADMIN_EMAIL = config('ADMIN_EMAIL', default='gregdyche@creighton.edu')

# Email for notifications about new subscriptions
SUBSCRIPTION_NOTIFICATION_EMAIL = ADMIN_EMAIL

