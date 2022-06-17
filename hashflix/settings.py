import os.path
from pathlib import Path

import storages.backends.s3boto3
from decouple import config, Csv
from dj_database_url import parse
from functools import partial

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'filme',
    'crispy_forms',
    'crispy_bootstrap5',
    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hashflix.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'filme.novos_context.lista_filmes_recentes',
                'filme.novos_context.lista_filmes_populares',
            ],
        },
    },
]

WSGI_APPLICATION = 'hashflix.wsgi.application'

# Database

default_db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

parse_database = partial(parse, conn_max_age=600)
DATABASES = {
    'default': config('DATABASE_URL', default=default_db_url, cast=parse_database)
}

# Password validation

AUTH_USER_MODEL = "filme.Usuario"

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

# configuração de ambiente de desenvolvimento
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default=False)

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'filme:homefilmes'
LOGIN_URL = 'filme:login'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

# configuração do S3

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

DISABLE_COLLECTSTATIC=1
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'



