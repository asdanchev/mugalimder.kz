from pathlib import Path
import os

import dj_database_url


# === Base ===
BASE_DIR = Path(__file__).resolve().parent.parent  # /app/src

DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-placeholder")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv("DJANGO_ALLOWED_HOSTS", "mugalimder.kz,www.mugalimder.kz").split(",")
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    "https://mugalimder.kz",
    "https://www.mugalimder.kz",
]


# === Apps ===
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd-party
    "django_extensions",

    # Local
    "profiles",
    "core",
    "users",
    'materials',
]


# === Middleware ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# === URLs / WSGI ===
ROOT_URLCONF = "mugalimder.urls"
WSGI_APPLICATION = "mugalimder.wsgi.application"


# === Templates ===
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "mugalimder" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# === Database ===
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# === Password validation ===
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# === i18n / tz ===
LANGUAGE_CODE = "ru"
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "Asia/Almaty")
USE_I18N = True
USE_TZ = True


# === Static / Media ===
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"


# === Auth redirects ===
LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


# === Other ===
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"