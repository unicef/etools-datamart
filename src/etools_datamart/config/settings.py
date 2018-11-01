# -*- coding: utf-8 -*-
import datetime
import os
from pathlib import Path

import environ

from etools_datamart.libs.dbrouter import router_factory

SETTINGS_DIR = Path(__file__).parent
PACKAGE_DIR = SETTINGS_DIR.parent
DEVELOPMENT_DIR = PACKAGE_DIR.parent.parent

env = environ.Env(API_URL=(str, 'http://localhost:8000/api/'),
                  ETOOLS_DUMP_LOCATION=(str, str(PACKAGE_DIR / 'apps' / 'multitenant' / 'postgresql')),

                  CACHE_URL=(str, "redis://127.0.0.1:6379/1"),
                  API_CACHE_URL=(str, "locmemcache://"),
                  # CACHE_URL=(str, "dummycache://"),
                  # API_CACHE_URL=(str, "dummycache://"),

                  ENABLE_LIVE_STATS=(bool, True),
                  CELERY_BROKER_URL=(str, 'redis://127.0.0.1:6379/2'),
                  CELERY_RESULT_BACKEND=(str, 'redis://127.0.0.1:6379/3'),
                  CSRF_COOKIE_SECURE=(bool, True),
                  DATABASE_URL=(str, "postgres://postgres:@127.0.0.1:5432/etools_datamart"),
                  DATABASE_URL_ETOOLS=(str, "postgis://postgres:@127.0.0.1:15432/etools"),
                  DEBUG=(bool, False),
                  MEDIA_ROOT=(str, '/tmp/media'),
                  SECRET_KEY=(str, 'secret'),
                  SECURE_HSTS_PRELOAD=(bool, 'True'),
                  SECURE_SSL_REDIRECT=(bool, True),
                  SECURE_BROWSER_XSS_FILTER=(bool, True),
                  SECURE_CONTENT_TYPE_NOSNIFF=(bool, True),
                  SECURE_FRAME_DENY=(bool, True),
                  SESSION_COOKIE_SECURE=(bool, True),
                  STATIC_ROOT=(str, '/tmp/static'),
                  X_FRAME_OPTIONS=(str, 'DENY'),

                  AZURE_CLIENT_ID=(str, ''),
                  AZURE_CLIENT_SECRET=(str, ''),
                  AZURE_TENANT=(str, ''),

                  )

DEBUG = env.bool('DEBUG')
if DEBUG:  # pragma: no cover
    env_file = env.path('ENV_FILE_PATH', default=DEVELOPMENT_DIR / '.env')
    environ.Env.read_env(str(env_file))

MEDIA_ROOT = env('MEDIA_ROOT')
STATIC_ROOT = env('STATIC_ROOT')

SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS', default=[]))

ADMINS = (
    ('', 'saxix@saxix.onmicrosoft.com'),
    ('', 'sapostolico@unicef.org'),
    ('', 'sapostolico@nikunicef.onmicrosoft.org'),

)

DATABASES = {
    'default': env.db(),
    'etools': env.db('DATABASE_URL_ETOOLS', engine='etools_datamart.apps.multitenant.postgresql'),
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
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# If you set this to False, Django will make some optimizations so as not
# to load the ernationalization machinery.
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.RemoteUserMiddleware',
    'crashlog.middleware.CrashLogMiddleware',
    'etools_datamart.api.middleware.ApiMiddleware',
    # 'etools_datamart.apps.tracking.middleware.ThreadedStatsMiddleware',
    'etools_datamart.apps.tracking.middleware.StatsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.azuread_tenant.AzureADTenantOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

CACHES = {
    'default': env.cache(),
    'api': env.cache('API_CACHE_URL')
}

ROOT_URLCONF = 'etools_datamart.config.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'etools_datamart.config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(PACKAGE_DIR / 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'etools_datamart.apps.multitenant.context_processors.schemas',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
                'i18n': 'django.templatetags.i18n',
            },
        },
    },
]
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

INSTALLED_APPS = [
    'etools_datamart.apps.web.apps.Config',
    'etools_datamart.apps.init.apps.Config',
    'etools_datamart.apps.multitenant',
    'etools_datamart.apps.security',

    'constance',
    'constance.backends.database',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'admin_extra_urls',
    'unicef_rest_framework',
    'rest_framework',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    'unicef_security',
    'django_filters',
    'month_field',

    'drf_yasg',
    'adminfilters',
    'django_db_logging',
    'django_sysinfo',
    'crashlog',

    'django_celery_beat',

    'etools_datamart.apps.core',
    'etools_datamart.apps.etools',
    'etools_datamart.apps.data',
    'etools_datamart.apps.etl.apps.Config',
    'etools_datamart.apps.tracking.apps.Config',
    'etools_datamart.api',
]

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
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_FRAME_DENY = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT')
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE')
X_FRAME_OPTIONS = env('X_FRAME_OPTIONS')

NOTIFICATION_SENDER = "etools_datamart@unicef.org"
EMAIL_SUBJECT_PREFIX = "[ETOOLS-DATAMART]"

# django-constance
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_ADDITIONAL_FIELDS = {
    # 'read_only_text': ['django.forms.fields.CharField', {
    #     'required': False,
    #     'widget': 'etools_datamart.libs.constance.ObfuscatedInput',
    # }],
    # 'write_only_text': ['django.forms.fields.CharField', {
    #     'required': False,
    #     'widget': 'etools_datamart.libs.constance.WriteOnlyTextarea',
    # }],
    # 'write_only_input': ['django.forms.fields.CharField', {
    #     'required': False,
    #     'widget': 'etools_datamart.libs.constance.WriteOnlyInput',
    # }],
    'select_group': ['etools_datamart.libs.constance.GroupChoiceField', {
        'required': False,
        'widget': 'etools_datamart.libs.constance.GroupChoice',
    }],
}

CONSTANCE_CONFIG = {
    'AZURE_USE_GRAPH': (True, 'Use MS Graph API to fetch user data', bool),
    'DEFAULT_GROUP': ('Guests', 'Use MS Graph API to fetch user data', 'select_group'),
}

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_TIMEZONE = 'America/New_York'
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULE = {}

CONCURRENCY_IGNORE_DEFAULT = False

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "PAGE_SIZE": 100,
    # "DEFAULT_PAGINATION_CLASS": 'rest_framework.pagination.CursorPagination',
    'DEFAULT_PAGINATION_CLASS': 'unicef_rest_framework.pagination.APIPagination',
    'DEFAULT_METADATA_CLASS': 'etools_datamart.api.metadata.SimpleMetadataWithFilters',
    # 'DEFAULT_SCHEMA_CLASS': 'etools_datamart.api.swagger.APIAutoSchema',
    # 'EXCEPTION_HANDLER': 'my_project.my_app.utils.custom_exception_handler'
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
}

AZURE_SSL = True
AZURE_URL_EXPIRATION_SECS = 10800
AZURE_ACCESS_POLICY_EXPIRY = 10800  # length of time before signature expires in seconds
AZURE_ACCESS_POLICY_PERMISSION = 'r'
AZURE_TOKEN_URL = 'https://login.microsoftonline.com/unicef.org/oauth2/token'
AZURE_GRAPH_API_BASE_URL = 'https://graph.microsoft.com'
AZURE_GRAPH_API_VERSION = 'v1.0'
AZURE_GRAPH_API_PAGE_SIZE = 300

JWT_AUTH = {
    'JWT_VERIFY': False,  # this requires private key
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 60,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=30000),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',

    # Keys will be set in core.apps.Config.ready()
    'JWT_PUBLIC_KEY': os.environ,
    # 'JWT_PRIVATE_KEY': wallet.get_private(),
    # 'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'RS256',

}

# social auth
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email']
SOCIAL_AUTH_SANITIZE_REDIRECTS = False
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_WHITELISTED_DOMAINS = ['unicef.org', 'google.com']
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
    'unicef_security.azure.default_group',
)

SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = env.str('AZURE_CLIENT_ID')
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = env.str('AZURE_CLIENT_SECRET')
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = env.str('AZURE_TENANT')
SOCIAL_AUTH_AZUREAD_OAUTH2_KEY = env.str('AZURE_CLIENT_ID')
# POLICY = os.getenv('AZURE_B2C_POLICY_NAME', "b2c_1A_UNICEF_PARTNERS_signup_signin")
SCOPE = ['openid', 'email']
IGNORE_DEFAULT_SCOPE = True

SWAGGER_SETTINGS = {
    'DEFAULT_API_URL': env('API_URL'),
    'DEFAULT_AUTO_SCHEMA_CLASS': 'etools_datamart.api.swagger.schema.APIAutoSchema',
    'DEFAULT_FILTER_INSPECTORS': ['etools_datamart.api.swagger.filters.APIFilterInspector', ],
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        'token': {
            'type': 'basic'
        }

    }
}

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_OBJECT_CACHE_KEY_FUNC':
        'rest_framework_extensions.utils.default_object_cache_key_func',
    'DEFAULT_LIST_CACHE_KEY_FUNC':
        'rest_framework_extensions.utils.default_list_cache_key_func',
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
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },

        'db': {
            'level': 'ERROR',
            'class': 'django_db_logging.handlers.DBHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'ERROR'
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False
        },
        'django_db_logging': {
            'handlers': ['console'],
            'level': {True: 'DEBUG', False: 'ERROR'}[DEBUG],
            'propagate': False
        },
        'drf_querystringfilter': {
            'handlers': ['console', 'db'],
            'level': 'DEBUG',
            'propagate': False
        },
        'unicef_rest_framework': {
            'handlers': ['console', 'db'],
            'level': 'ERROR',
            'propagate': False
        },
        'etools_datamart': {
            'handlers': ['console', 'db'],
            'level': 'ERROR',
            'propagate': False
        },
    },
}

LOGGING_DEBUG = {
    'version': 1,
    'disable_existing_loggers': True,
}

TENANT_MODEL = 'etools.UsersCountry'
ETOOLS_DUMP_LOCATION = env('ETOOLS_DUMP_LOCATION')

UNICEF_REST_FRAMEWORK_ROUTER = 'etools_datamart.api.urls.router'

SCHEMA_FILTER = {}
SCHEMA_EXCLUDE = {'schema_name__in': ['public', 'uat', 'frg']}

ENABLE_LIVE_STATS = env('ENABLE_LIVE_STATS')

BUSINESSAREA_MODEL = 'unicef_security.BusinessArea'
AUTH_USER_MODEL = 'unicef_security.User'
