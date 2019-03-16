"""
Django settings for MoodyHumans project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import django_heroku
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('MH_SECRET_KEY')

# Application definition

INSTALLED_APPS = [
    'measurements.apps.MeasurementsConfig',
    'questionnaires.apps.QuestionnairesConfig',
    # Dependencies:
    'django_extensions',
    # 'rest_framework',
    'django_simple_bulma',
    'openhumans',
    # Defaults:
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'moodyhumans.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'moodyhumans.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGOUT_REDIRECT_URL = '/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = '/moodyhumans/static'
STATIC_URL = '/static/'

STATICFILES_FINDERS = [
  # Defaults
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  # Bulma
  'django_simple_bulma.finders.SimpleBulmaFinder',
]

BULMA_SETTINGS = {
    "variables": {
        'widescreen-enabled': 'false',
        'fullhd-enabled': 'false',
        'desktop': '769px',
        'widescreen': '769px',
        'fullhd': '769px'
    }
}

# Deployment checks

CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
X_FRAME_OPTIONS = 'DENY'

# Openhumans
# See: https://django-open-humans.readthedocs.io/en/latest/modules/getting-started.html

OPENHUMANS_APP_BASE_URL = os.getenv('OPENHUMANS_APP_BASE_URL')
OPENHUMANS_CLIENT_ID = os.getenv('OPENHUMANS_CLIENT_ID')
OPENHUMANS_CLIENT_SECRET = os.getenv('OPENHUMANS_CLIENT_SECRET')
OPENHUMANS_OH_BASE_URL = os.getenv('OPENHUMANS_OH_BASE_URL')

django_heroku.settings(locals())