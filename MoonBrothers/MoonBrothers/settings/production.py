from .base import *

DEBUG = True

ALLOWED_HOSTS = ['5.180.106.89']

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