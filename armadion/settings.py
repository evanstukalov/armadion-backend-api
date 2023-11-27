"""
Django settings for armadion project.
"""

import os
from pathlib import Path

# For setup Environment Variables
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS').split(" ")

# Application definition

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # My apps
    'contactform',
    'doors',
    # Rest framework
    'rest_framework',
    # Plugins
    'phonenumber_field',  # for phone number
    'drf_yasg',  # for swagger documentation
    'corsheaders',
    'django_filters',
    # 'debug_toolbar',
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
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'armadion.urls'

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

WSGI_APPLICATION = 'armadion.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env.str("DB_ENGINE"),
        'NAME': env.str("DB_NAME"),
        'USER': env.str("DB_USER"),
        'PASSWORD': env.str("DB_PASSWORD"),
        'HOST': env.str("DB_HOST"),
        'PORT': env("DB_PORT"),
    }
}

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

REST_FRAMEWORK = {
  'EXCEPTION_HANDLER': 'utils.exceptionhandler.custom_exception_handler',
}


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


LANGUAGE_CODE = 'ru-ru'

DATETIME_FORMAT = ("%Y-%m-%d", "%H:%M:%S")

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

CSRF_TRUSTED_ORIGINS = [
    "http://0.0.0.0:1337",
    "http://localhost:1337",
    "http://185.244.51.158:80"
]

CORS_ALLOWED_ORIGINS = [
    "http://0.0.0.0:1337",
    "http://localhost:1337",
    "http://185.244.51.158:80",
]
# For debug toolbar
# INTERNAL_IPS = [
#    '127.0.0.1',
#    '0.0.0.0',
# ]
## For debug toolbar
# DEBUG_TOOLBAR_CONFIG = {
#    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
# }

CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOW_CREDENTIALS = True



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# logger config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[{name}] [{levelname}] [{asctime}] [{message}]',
            'style': '{',
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': BASE_DIR / 'debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
        }
    }
}

# celery broker and result
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", default="redis://redis:6379/0")


