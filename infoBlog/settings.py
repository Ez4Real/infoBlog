"""
Django settings for infoBlog project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os

from pathlib import Path
from dotenv import load_dotenv

from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = BASE_DIR / 'config/.env'
load_dotenv(dotenv_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DJANGO_DEBUG', True))

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(" ")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'ckeditor',
    'ckeditor_uploader',
    'cloudinary_storage',
    'cloudinary',
    'phonenumber_field',
    'ordered_model',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'infoBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'infoBlog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'blog.backends.LibraryMemberAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True
USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('uk', _('Ukrainian')),
    ('en', _('English')),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/ergosum/ergosum-europa.eu/public/static/'

# Ckeditor Code Snippet
CKEDITOR_UPLOAD_PATH = 'uploads'
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_BROWSE_SHOW_DIRS = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ','.join(
            [
               'html5video',
            ]
        ),
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Emailing settings
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'smtp.dreamhost.com'
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_FROM')
EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_HOST_USER = os.getenv('EMAIL_FROM')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 465
EMAIL_USE_TLS = True

PASSWORD_RESET_TIMEOUT = 14400

CSRF_TRUSTED_ORIGINS = ['https://' + host for host in os.getenv('DJANGO_ALLOWED_HOSTS').split()]

# Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'),
    'API_KEY': os.getenv('API_KEY'),
    'API_SECRET': os.getenv('API_SECRET')
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Secure
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = bool(os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS'))
SECURE_HSTS_PRELOAD = bool(os.getenv('SECURE_HSTS_PRELOAD'))
SECURE_SSL_REDIRECT = bool(os.getenv('SECURE_SSL_REDIRECT'))
SESSION_COOKIE_SECURE = bool(os.getenv('SESSION_COOKIE_SECURE'))
CSRF_COOKIE_SECURE = bool(os.getenv('CSRF_COOKIE_SECURE'))

# blog underhood settings
POSTS_PER_PAGE = 15
RES_PER_PAGE = 16
TITLE = _('European Research Group Of Support for Ukrainian Membership – ERGOSUM')
HOMEPAGE_CONTENT = (
    (5, 'News', 'carousel_news'),
    (3, 'News', 'last_news'),
    (3, 'Op-eds', 'last_opeds'),
    (3, 'Analytics', 'last_analytics'),
    (3, 'Opinion', 'last_opinions'),
)
