"""
Django settings for ebr_project project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from django.contrib.messages import constants as messages
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['54.213.76.238', '127.0.0.1', 'localhost']

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django third party lib
    'widget_tweaks',
    'crispy_forms',
    'ckeditor',
    'ckeditor_uploader',
    'extra_views',
    # User define application
    'core.apps.CoreConfig',
    'frontend.apps.FrontendConfig',
    # S3Bucket lib
    'storages',
    # Sitemap lib
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'debug_toolbar',
    'api',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'ebr_project.urls'

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
                # 'core.utils.context_processors.settings_context',
                'core.context_processors.settings_context',
                'frontend.context_processor.footer_links',
                'frontend.context_processor.navbar_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'ebr_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('PORT')
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'

# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

IFRAME_URL = config('iframe_url')
IFRAME_API_KEY = config('iframe_API_key')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Change message color using below commend.
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Give project title.
PROJECT_TITLE = "EBR"
COPYRIGHT = "EBR"
META_URL = "ElectricBikeReview.com"

# Define login, logout, and Auth user model here.
AUTH_USER_MODEL = "core.user"
LOGIN_URL = "auth:auth_login"
LOGIN_REDIRECT_URL = "/customadmin"
LOGOUT_REDIRECT_URL = "auth:auth_login"

# S3Bucket Configuration below
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_REGION_NAME = config('DJANGO_REGION')
AWS_ACCESS_KEY_ID = config('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('DJANGO_AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = 'public-read'
AWS_IMAGE_URL = 'https://ebr-dev-bucket.s3.amazonaws.com/'

# Define Ckeditor menu and toolbar.

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "ckeditor_uploader.backends.PillowBackend"
CKEDITOR_THUMBNAIL_SIZE = (300, 300)
CKEDITOR_IMAGE_QUALITY = 40
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_ALLOW_NONIMAGE_FILES = True

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Pro",
        "toolbar_Pro": [
            [
                # "Undo",
                # "Redo",
                # "-",
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "-",
                "NumberedList",
                "BulletedList",
                # "-",
                # "JustifyLeft",
                # "JustifyCenter",
                # "JustifyRight",
                # "JustifyBlock",
                "-",
                "Link",
                # "Unlink",
                # "Anchor",
                "-",
                # "Image",
                # "Table",
                # "HorizontalRule",
                # "SpecialChar",
                # "-",
                # "TextColor",
                # "BGColor",
                "-",
                "Source",
            ]
        ],
        "toolbar_Simple": [["Source", "-", "Bold", "Italic", "BulletedList"]],
        "tabSpaces": 4,
        'basicEntities': False,
        'htmlEncodeOutput': False,
        'entities': False,
        'removeDialogTabs': 'link:upload;image:Upload;link:Advanced;link:Target;link:info:browse;',
    },
}

SCHEMA_URL = 'https://electricbikereview.com'

PYTHON_AKISMET_API_KEY = config('PYTHON_AKISMET_API_KEY')
PYTHON_AKISMET_BLOG_URL = config('PYTHON_AKISMET_BLOG_URL')

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_HOST_USER = 'b1c20aaaf2cf30'
EMAIL_HOST_PASSWORD = '4e486fd5279af7'
EMAIL_USE_TLS = True

SITE_ID = 1
