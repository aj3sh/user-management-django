"""
Django settings for user_management project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import environ
from datetime import timedelta
from pathlib import Path

# loading environment
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', default='django-insecure-$zx26p_yum0+0)n$$o$x2g4jtls^6mk*m&&u4qt4%03k6tion-')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
	'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'users',
    'users.api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'user_management.urls'

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

WSGI_APPLICATION = 'user_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
	'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3'),
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

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User
AUTH_USER_MODEL = 'users.User'


# REST FRAMEWORK AND JWT SETTINGS
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}


# Logging
LOG_FILE_PATH = env.str('LOG_FILE_PATH', default=BASE_DIR / 'log/debug.log')

# creating directory
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
with open(LOG_FILE_PATH, "w") as f:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
		'standard': {
			'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
			'datefmt' : "%Y-%b-%d %H:%M:%S"
		},
	},
    'handlers': {
        'null': {
			'level':'DEBUG',
			'class':'logging.NullHandler',
		},
		'logfile': {
			'level':'DEBUG',
			'class':'logging.handlers.RotatingFileHandler',
			'filename': LOG_FILE_PATH,
			'maxBytes': 50000,
			'backupCount': 50,
			'formatter': 'standard',
		},
		'console':{
			'level':'INFO',
			'class':'logging.StreamHandler',
			'formatter': 'standard'
		},
    },
    'loggers': {
		'django': {
			'handlers':['console'],
			'propagate': True,
			'level':'WARN',
		},
		'users': {
			'handlers': ['console', 'logfile'],
			'level': 'DEBUG',
		},
	}
}


# CORS
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'Access-Control-Allow-Origin',
    'Access-Control-Allow-Headers',
    'Authorization',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)