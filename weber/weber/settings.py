"""
Django settings for weber project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


os.environ['DJANGO_SETTINGS_MODULE'] = 'weber.settings'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DBNAME = 'test'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ujhjqrlel9*wf!**23by@ukbk19^gnv0og$#-8=6!3#huawiw7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = (
        'mongoengine.django.auth.MongoEngineBackend',
)
LOGIN_URL = '/theweber.in/login'
LOGIN_REDIRECT_URL = '/theweber.in/login'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'mongoengine.django.mongo_auth',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'home_func',
    'djangular',
    'gunicorn',
    'myapp',

)

REDIS_SSEQUEUE_CONNECTION_SETTINGS = {
    'location': 'localhost:6379',
    'db': 0,
}


MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'
AUTH_USER_MODEL = 'mongo_auth.MongoUser'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'weber.urls'

WSGI_APPLICATION = 'weber.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}


SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, '../templates'),)


"""TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join( BASE_DIR, 'templates' )
)"""
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = ''

#eamil sending details of smtp server
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'suryachowdary93@gmail.com'

EMAIL_HOST_PASSWORD = '9014639760'

EMAIL_PORT = 587

EMAIL_USE_TLS = True