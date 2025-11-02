#!/bin/sh
set -e

# создаём Django-проект при первом старте, если его нет
if [ ! -f "/app/manage.py" ]; then
  django-admin startproject mugalimder /app
  # Патчим settings.py (DB, ALLOWED_HOSTS, static, CSRF, WhiteNoise)
  py=/app/mugalimder/settings.py
  sed -i "s/DEBUG = True/DEBUG = False/g" "$py"

  # Добавляем импорты и env
  cat >> "$py" << 'PYEOF'

import os
import dj_database_url

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "insecure")
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()]

CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS","").split(",") if o.strip()]

STATIC_URL = '/static/'
STATIC_ROOT = os.getenv("STATIC_ROOT", "/app/static")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv("MEDIA_ROOT", "/app/media")

DATABASES = {
    'default': dj_database_url.parse(os.getenv("DATABASE_URL","sqlite:////app/db.sqlite3"), conn_max_age=600)
}

INSTALLED_APPS += ['whitenoise.runserver_nostatic']
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE
PYEOF
fi

python /app/manage.py migrate --noinput
python /app/manage.py collectstatic --noinput

exec gunicorn mugalimder.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
