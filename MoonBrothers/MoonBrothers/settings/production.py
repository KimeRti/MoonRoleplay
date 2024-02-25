from .base import *

DEBUG = False

ALLOWED_HOSTS = ['5.180.106.89','moonroleplaytr.com','www.moonroleplaytr.com']

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