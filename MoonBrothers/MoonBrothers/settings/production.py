from .base import *

DEBUG = False

ALLOWED_HOSTS = ['www.deryamakine.com', 'deryamakine.com']

STATIC_ROOT = 'MoonBrothers/static/'

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'moonrp',

        'USER': 'detex',

        'PASSWORD': 'detex123',

        'HOST': 'localhost',

        'PORT': '5432',

    }
}