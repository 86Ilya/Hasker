import os

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG = True
DB_PORT = os.environ.get('HASKER_DB_PORT')
DB_HOST = os.environ.get('HASKER_DB_HOST')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hasker_db',
        'USER': 'hasker',
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}