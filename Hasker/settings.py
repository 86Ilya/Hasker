import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
if SECRET_KEY is None:
    print("SECRET_KEY NOT FOUND! PLEASE PROVIDE VALID SECRET_KEY")
    os.sys.exit(1)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'rest_framework.authtoken',
    'rest_framework_swagger',

    'Hasker.profile',
    'Hasker.hasker',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'USE_SESSION_AUTH': False,
}

ROOT_URLCONF = 'Hasker.urls'
TEMPLATE_DIR = os.path.join(BASE_DIR, "Hasker/templates")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
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

WSGI_APPLICATION = 'Hasker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DB_PORT = '5432'
DB_HOST = ''

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


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ilya.aurov.testing@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "Hasker", "staticfiles"),
    os.path.join(BASE_DIR, "Hasker", "media"),
]

STATIC_URL = '/static/'

LOGIN_URL = '/login/'
MEDIA_ROOT = os.path.join(BASE_DIR, "Hasker", "media")
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
AUTH_USER_MODEL = "profile.HaskerUser"

# Display settings
# Количество вопросов отображаемых в колонке справа
TRENDING_QUESTIONS = 20
# Максимальное количество вопросов отображаемых на одной странице
QUESTIONS_PER_PAGE = 20
# Максимальное количество ответов отображаемых на одной странице
ANSWERS_PER_PAGE = 30
# Максимальная длинна запроса на поиск
MAX_LENGTH_SEARCH = 1024


try:
    from .local_settings import *  # noqa: F401 F403
    print("Using local settings. Remove it in production!")
except ImportError as error:
    print(error)
