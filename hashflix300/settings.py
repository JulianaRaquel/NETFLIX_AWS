import os.path
from pathlib import Path
from dj_database_url import parse
from decouple import config, Csv
from functools import partial

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
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
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

default_db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

parse_data = partial(parse, conn_max_age=600)
DATABASES = {
    'default': config('DATABASE_URL', default=default_db_url, cast=parse_data)
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# configuração de ambiente de desenvolvimento
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

COLLECTFAST_ENABLED = False

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default=False)

# configuração para o S3

if AWS_ACCESS_KEY_ID:
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}
    AWS_PRELOAD_METADATA = True
    AWS_AUTO_CREATE_BUCKET = False
    AWS_QUERYSTRING_AUTH = True
    AWS_S3_CUSTOM_DOMAIN = None
    AWS_DEFAULT_ACL = 'private'

    COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
    COLLECTFAST_ENABLED = True

    # configurações dos arquivos estáticos
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    STATIC_S3_PATH = 'static'
    STATIC_ROOT = f'/{STATIC_S3_PATH}/'
    STATIC_URL = f'//s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{STATIC_S3_PATH}/'
    ADMIN_MEDIA_PREFIX = STATIC_URL + '/admin'

    # configurações dos uploads de arquivos
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.StaticStorage'
    DEFAULT_S3_PATH = 'media'
    MEDIA_ROOT = f'/{DEFAULT_S3_PATH}/'
    MEDIA_URL = f'//s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{DEFAULT_S3_PATH}/'

    INSTALLED_APPS.append('s3_folder_storage')
    INSTALLED_APPS.append('storages')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'filme:homefilmes'
LOGIN_URL = 'filme:login'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

# https://github.com/django-crispy-forms/crispy-bootstrap5