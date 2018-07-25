# -*- coding: utf-8 -*-

import logging
import os
from pathlib import Path

import environ

import etools_datamart
from etools_datamart.libs.dbrouter import router_factory

env = environ.Env(DEBUG=(bool, False),
                  SECRET_KEY=(str, 'secret'),
                  DATABASE_URL=(str, "postgres://postgres:@127.0.0.1:5432/etools_datamart"),
                  DATABASE_URL_ETOOLS=(str, "postgis://postgres:@127.0.0.1:15432/etools"),
                  CACHE_URL=(str, "locmemcache://"),
                  MEDIA_ROOT=(str, '/tmp/media'),
                  STATIC_ROOT=(str, '/tmp/static'),

                  SECURE_SSL_REDIRECT=(bool, True),
                  CSRF_COOKIE_SECURE=(bool, True),
                  SESSION_COOKIE_SECURE=(bool, True),
                  )

SETTINGS_DIR = Path(__file__).parent
SOURCE_DIR = SETTINGS_DIR.parent.parent.parent
env_file = env.path('ENV_FILE_PATH', default=SOURCE_DIR / '.env')

# if Path(str(env_file)).exists():  # pragma: no cover
environ.Env.read_env(str(env_file))

MEDIA_ROOT = env('MEDIA_ROOT')
STATIC_ROOT = env('STATIC_ROOT')

DEBUG = env('DEBUG')  # False if not in os.environ
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS', default=[]))

ADMINS = (

)

DATABASES = {
    # 'default': env.db(),
    # 'etools': env.db('DATABASE_URL_ETOOLS'),
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'etools_datamart',
        'HOST': '127.0.0.1',
        'USER': 'postgres',
        'PORT': '',
        'OPTIONS': {
            'options': '-c search_path=public'
        },
    },
    'etools': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'etools_datamart.libs.postgresql',
        'NAME': 'etools',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '15432',
        # 'TEST': {
        #     'NAME': 'etools',
        # }
        # 'OPTIONS': {
        #     'options': '-c search_path=bolivia,public'
        # },
    },
}


DATABASE_ROUTERS = [
    # 'tenant_schemas.routers.TenantSyncRouter',
    # router_factory('default', ['default'], syncdb=True),
    router_factory('etools', ['etools'], syncdb=False),
]

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'
ugettext = lambda s: s  # noqa
LANGUAGES = (
    ('es', ugettext('Spanish')),
    ('fr', ugettext('French')),
    ('en', ugettext('English')),
    ('ar', ugettext('Arabic')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(PROJECT_DIR, '../static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'etools_datamart.apps.core.middleware.ApiMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

CACHES = {
    'default': env.cache()
}

ROOT_URLCONF = 'etools_datamart.config.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'etools_datamart.config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': False,
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
                'i18n': 'django.templatetags.i18n',
            },
        },
    },
]
AUTH_USER_MODEL = 'auth.User'
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

INSTALLED_APPS = [
    'etools_datamart.apps.init',

    # 'constance',
    # 'constance.backends.database',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'raven.contrib.django.raven_compat',

    'rest_framework',
    'rest_framework.authtoken',
    'unicef_rest_framework',

    'etools_datamart.apps.core',
    'etools_datamart.apps.etools',
    'etools_datamart.api',
]

# R_APPS = ['etools_datamart.apps.etools']


DATE_INPUT_FORMATS = [
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',  # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',  # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
]

DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',  # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',  # '2006-10-25 14:30'
    '%Y-%m-%d',  # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',  # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',  # '10/25/2006 14:30'
    '%m/%d/%Y',  # '10/25/2006'
    '%m/%d/%y %H:%M:%S',  # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',  # '10/25/06 14:30'
    '%m/%d/%y',  # '10/25/06'
]

# django-secure
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT')
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE')
SECURE_HSTS_SECONDS = 1
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE')
SESSION_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

NOTIFICATION_SENDER = "sir@unicef.org"
EMAIL_SUBJECT_PREFIX = "[SIR]"

RAVEN_CONFIG = {
    'CELERY_LOGLEVEL': logging.INFO,
    'release': etools_datamart.VERSION,
}

# django-constance
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
}

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_RESULT_BACKEND = 'django_celery_results.backends.database:DatabaseBackend'
CELERY_TIMEZONE = 'America/New_York'
CELERY_BROKER_URL = 'redis://'

CONCURRENCY_IGNORE_DEFAULT = False

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    )
}

LOG_DIR = os.environ.get('SIR_LOG_DIR',
                         os.path.expanduser('~/logs'))

os.makedirs(LOG_DIR, exist_ok=True)


def file_handler(name, level):
    return {
        'level': level,
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': 'full',
        'filename': os.path.join(LOG_DIR, '%s.log' % name),
    }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'full': {
            'format': '%(levelname)-8s: %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'verbose': {
            'format': '%(levelname)-8s: %(asctime)s %(name)20s %(message)s'
        },
        'simple': {
            'format': '%(levelname)-8s: %(asctime)s %(name)20s: %(funcName)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'errors': file_handler('errors', 'DEBUG'),
        'security': file_handler('security', 'DEBUG'),
        'business': file_handler('business', 'DEBUG'),
        'root': file_handler('messages', 'DEBUG'),
        'application': file_handler('sir', 'DEBUG'),
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['root'],
            'propagate': True,
            'level': 'ERROR'
        },
        'django.request': {
            'handlers': ['root'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['root'],
            'level': 'ERROR',
            'propagate': True
        },
        'errors': {
            'handlers': ['errors'],
            'level': 'ERROR',
            'propagate': True
        },
        'exceptions': {
            'handlers': ['errors'],
            'level': 'ERROR',
            'propagate': True
        },
        'security': {
            'handlers': ['security'],
            'level': 'INFO',
            'propagate': False
        },
        'testing': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'sir': {
            'handlers': ['application'],
            'level': 'ERROR',
            'propagate': True
        },
        'sir.settings': {
            'handlers': ['application'],
            'level': 'ERROR',
            'propagate': True
        },
        'raven': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

LOGGING_DEBUG = {
    'version': 1,
    'disable_existing_loggers': True,
}
