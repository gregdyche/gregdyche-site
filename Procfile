web: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py update_site_domain && gunicorn gregdyche.wsgi:application --bind 0.0.0.0:$PORT
