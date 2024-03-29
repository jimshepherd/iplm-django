"""
Django settings for iplm project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import environ
import google.auth
from google.cloud import secretmanager
import io
import os
from pathlib import Path
from urllib.parse import urlparse


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(None, '*'),
    CORS_ALLOWED_ORIGINS=(list, []),
    STATIC_ROOT=(str, None),
)

env_file = os.path.join(BASE_DIR, '.env')

# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ['GOOGLE_CLOUD_PROJECT'] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass

if os.path.isfile(env_file):
    # Use a local secret file, if provided

    env.read_env(env_file)
# [START_EXCLUDE]
elif os.getenv('TRAMPOLINE_CI', None):
    # Create local settings if running with CI, for unit testing

    placeholder = (
        f'SECRET_KEY=a\n'
        'GS_BUCKET_NAME=None\n'
        f'DATABASE_URL=sqlite://{os.path.join(BASE_DIR, "db.sqlite3")}'
    )
    env.read_env(io.StringIO(placeholder))
# [END_EXCLUDE]
elif os.environ.get('GOOGLE_CLOUD_PROJECT', None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get('SETTINGS_NAME', 'django_settings')
    name = f'projects/{project_id}/secrets/{settings_name}/versions/latest'
    payload = client.access_secret_version(name=name).payload.data.decode('UTF-8')

    env.read_env(io.StringIO(payload))
else:
    raise Exception('No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.')
# [END cloudrun_django_secret_config]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# [START cloudrun_django_csrf]
# SECURITY WARNING: It's recommended that you use this when
# running in production. The URL will be known once you first deploy
# to Cloud Run. This code takes the URL and converts it to both these settings formats.
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    # Allow remote computers to access development
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
# [END cloudrun_django_csrf]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Required for GraphiQL
    'iplm_graphql.apps.IplmGraphqlConfig',
    # 'treebeard',
    'graphene_django',
    'corsheaders',
    'sortedm2m',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',

]

ROOT_URLCONF = 'iplm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            # BASE_DIR / 'venv/lib/python3.8/site-packages/treebeard/templates',
        ],
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

WSGI_APPLICATION = 'iplm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# [START cloudrun_django_database_config]
DATABASES = {
    'default': env.db(),
}

# If the flag as been set, configure to use proxy
if os.getenv('USE_CLOUD_SQL_AUTH_PROXY', None):
    DATABASES['default']['HOST'] = "127.0.0.1"
    DATABASES['default']['PORT'] = 5432

# [END cloudrun_django_database_config]


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
# [START cloudrun_django_static_config]
# Define static storage via django-storages[google]
GS_BUCKET_NAME = env('GS_BUCKET_NAME')
STATIC_URL = '/static/'
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_DEFAULT_ACL = 'publicRead'
# [END cloudrun_django_static_config]

STATIC_ROOT = env('STATIC_ROOT')

# For django_graphene
GRAPHENE = {
    'SCHEMA': 'iplm.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
