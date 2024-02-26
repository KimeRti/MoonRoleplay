from .base import *

DEBUG = True

ALLOWED_HOSTS = ['5.180.106.89','moonroleplaytr.com','www.moonroleplaytr.com']

CSRF_TRUSTED_ORIGINS = ['http://www.moonroleplaytr.com', 'http://moonroleplaytr.com', 'https://www.moonroleplaytr.com', 'https://moonroleplaytr.com']
CORS_ALLOWED_ORIGINS = ['http://www.moonroleplaytr.com', 'http://moonroleplaytr.com', 'https://www.moonroleplaytr.com', 'https://moonroleplaytr.com']
CORS_ALLOWED_ORIGIN_REGEXES = ['http://www.moonroleplaytr.com', 'http://moonroleplaytr.com', 'https://www.moonroleplaytr.com', 'https://moonroleplaytr.com']
CORS_ALLOW_ALL_ORIGINS = ['http://www.moonroleplaytr.com', 'http://moonroleplaytr.com', 'https://www.moonroleplaytr.com', 'https://moonroleplaytr.com']

STATIC_ROOT = 'MoonBrothers/static/'

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'moonrp',

        'USER': 'detexuser',

        'PASSWORD': 'detex123',

        'HOST': 'localhost',

        'PORT': '5432',

    }
}