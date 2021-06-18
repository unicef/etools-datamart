import datetime
import os
from pathlib import Path
from smtplib import SMTPServerDisconnected

import environ

from etools_datamart.libs.dbrouter import router_factory
from etools_datamart.libs.version import get_full_version

SETTINGS_DIR = Path(__file__).parent
PACKAGE_DIR = SETTINGS_DIR.parent
DEVELOPMENT_DIR = PACKAGE_DIR.parent.parent

env = environ.Env(API_PREFIX=(str, '/api/'),
                  ABSOLUTE_BASE_URL=(str, 'http://localhost:8000'),
                  ANALYTICS_CODE=(str, ""),
                  AUTOCOMMIT_EXTERNAL=(bool, True),
                  AZURE_CLIENT_ID=(str, ''),
                  AZURE_CLIENT_SECRET=(str, ''),
                  AZURE_STORAGE_ACCOUNT_KEY=(str, ''),
                  AZURE_STORAGE_ACCOUNT_NAME=(str, ''),
                  AZURE_STORAGE_OVERWRITE_FILES=(bool, True),
                  AZURE_STORAGE_CONTAINER=(str, ''),
                  AZURE_STORAGE_LOCATION=(str, ''),
                  AZURE_STORAGE_AUTO_SIGN=(bool, True),
                  AZURE_STORAGE_ACCESS_MODE=(str, "r"),
                  AZURE_STORAGE_ACCESS_TTL=(int, 60 * 60 * 24),
                  AZURE_TENANT=(str, ''),
                  CACHE_URL=(str, "redis://127.0.0.1:6379/1"),
                  CACHE_URL_API=(str, "redis://127.0.0.1:6379/2?key_prefix=api"),
                  CACHE_URL_LOCK=(str, "redis://127.0.0.1:6379/2?key_prefix=lock"),
                  CACHE_URL_TEMPLATE=(str, "redis://127.0.0.1:6379/2?key_prefix=template"),
                  CELERY_ALWAYS_EAGER=(bool, False),
                  CELERY_BROKER_URL=(str, 'redis://127.0.0.1:6379/2'),
                  CELERY_RESULT_BACKEND=(str, 'redis://127.0.0.1:6379/3'),
                  CSRF_COOKIE_SECURE=(bool, True),
                  EXPLORER_TOKEN=(str, 'EXPLORER_DATAMART_TOKEN'),
                  IGNORED_SCHEMAS=(str, ["public", "uat", "frg"]),
                  DATABASE_URL=(str, "postgis://postgres:@127.0.0.1:5432/etools_datamart"),
                  DATABASE_URL_ETOOLS=(str, "postgis://postgres:@127.0.0.1:5432/etools"),
                  DATABASE_URL_PRP=(str, "postgis://postgres:@127.0.0.1:5432/prp"),
                  DEBUG=(bool, False),
                  STACK=(str, 'DEVELOPMENT'),
                  API_PAGINATION_OVERRIDE_KEY=(str, 'disable-pagination'),
                  API_PAGINATION_SINGLE_PAGE_ENABLED=(bool, False),
                  DISABLE_SCHEMA_RESTRICTIONS=(bool, False),
                  DISABLE_SERVICE_RESTRICTIONS=(bool, False),
                  DISCONNECT_URL=(str, 'https://login.microsoftonline.com/unicef.org/oauth2/logout'),
                  EMAIL_HOST=(str, ''),
                  EMAIL_HOST_PASSWORD=(str, ''),
                  EMAIL_HOST_USER=(str, ''),
                  EMAIL_PORT=(int, 587),
                  EMAIL_USE_TLS=(bool, True),
                  ENABLE_LIVE_STATS=(bool, False),
                  ETOOLS_DUMP_LOCATION=(str, str(PACKAGE_DIR / 'apps' / 'multitenant' / 'postgresql')),
                  EXPORT_FILE_STORAGE=(str, 'unicef_rest_framework.storage.UnicefAzureStorage'),
                  EXPORT_FILE_STORAGE_KWARGS=(dict, {}),
                  GEOS_LIBRARY_PATH=(str, None),
                  GDAL_LIBRARY_PATH=(str, None),
                  MEDIA_ROOT=(str, '/tmp/media'),
                  MEDIA_URL=(str, '/media/'),
                  MYSTICA_PASSWORD=(str, ''),
                  REDOC_BASE=(str, '/api/+redoc/#operation/'),
                  SECRET_KEY=(str, 'secret'),
                  SECURE_BROWSER_XSS_FILTER=(bool, True),
                  SECURE_CONTENT_TYPE_NOSNIFF=(bool, True),
                  SECURE_FRAME_DENY=(bool, True),
                  SECURE_HSTS_PRELOAD=(bool, True),
                  SECURE_SSL_REDIRECT=(bool, True),
                  SENTRY_DSN=(str, ''),
                  SESSION_COOKIE_HTTPONLY=(bool, True),
                  SESSION_COOKIE_SECURE=(bool, True),
                  STATIC_ROOT=(str, '/tmp/static'),
                  STATIC_URL=(str, '/dm-static/'),
                  SYSTEM_PASSWORD=(str, ''),
                  TIME_ZONE=(str, 'UTC'),
                  URL_PREFIX=(str, ''),
                  USE_X_FORWARDED_HOST=(bool, False),
                  X_FRAME_OPTIONS=(str, 'DENY'),
                  GEONAMES_URL=(str, 'http://api.geonames.org/findNearbyJSON'),
                  GEONAMES_USERNAME=(str, 'ntrncic'),
                  REQUEST_TIMEOUT=(int, 300),
                  )

DEBUG = env.bool('DEBUG')
if DEBUG:  # pragma: no cover
    env_file = env.path('ENV_FILE_PATH', default=DEVELOPMENT_DIR / '.env')
    environ.Env.read_env(str(env_file))

SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
ABSOLUTE_BASE_URL = env('ABSOLUTE_BASE_URL')
API_PREFIX = env('API_PREFIX')
URL_PREFIX = env('URL_PREFIX')

DATABASES = {
    'default': env.db(),
    'etools': env.db('DATABASE_URL_ETOOLS',
                     engine='etools_datamart.apps.multitenant.postgresql'
                     ),
    'prp': env.db('DATABASE_URL_PRP')

}

# DATABASES['default']['CONN_MAX_AGE'] = 60
DATABASES['etools']['AUTOCOMMIT'] = env('AUTOCOMMIT_EXTERNAL')
DATABASES['prp']['AUTOCOMMIT'] = env('AUTOCOMMIT_EXTERNAL')

DATABASE_ROUTERS = [
    # 'tenant_schemas.routers.TenantSyncRouter',
    # router_factory('default', ['data', 'unicef_rest_framework',
    #                            'etl', 'security', 'unicef_security',
    #                            'auth', 'authtoken', 'contenttypes',
    #                            'django_db_logging'], syncdb=True),
    router_factory('etools', ['etools'], syncdb=False),
    router_factory('prp', ['source_prp'], syncdb=False),
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
API_PAGINATION_OVERRIDE_KEY = env('API_PAGINATION_OVERRIDE_KEY')
API_PAGINATION_SINGLE_PAGE_ENABLED = env('API_PAGINATION_SINGLE_PAGE_ENABLED')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = env('TIME_ZONE')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
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
MEDIA_ROOT = env('MEDIA_ROOT')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/dm-media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = env('STATIC_ROOT')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = env('STATIC_URL')

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(PROJECT_DIR, '../static'),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    # 'django.contrib.auth.middleware.RemoteUserMiddleware',
    'unicef_rest_framework.middleware.ApiMiddleware',
    # 'etools_datamart.apps.tracking.middleware.ThreadedStatsMiddleware',
    'etools_datamart.apps.tracking.middleware.StatsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    # 'social_core.backends.azuread_tenant.AzureADTenantOAuth2',
    'unicef_security.backends.UNICEFAzureADTenantOAuth2Ext',
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
]
MYSTICA_PASSWORD = env('MYSTICA_PASSWORD')

CACHES = {
    'default': env.cache(),
    'lock': env.cache('CACHE_URL_LOCK'),
    'api': env.cache('CACHE_URL_API'),
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
                'constance.context_processors.config',
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
GEOS_LIBRARY_PATH = env('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = env('GDAL_LIBRARY_PATH')

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
    'etools_datamart.apps.security.apps.Config',
    'constance',
    'constance.backends.database',
    'django.contrib.auth',
    'django.contrib.gis',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'etools_datamart.config.admin.AdminConfig',

    'etools_datamart.apps.core.apps.Config',
    'etools_datamart.apps.etl.apps.Config',
    'etools_datamart.apps.tracking.apps.Config',
    'etools_datamart.apps.subscriptions',
    'etools_datamart.apps.me',

    'etools_datamart.apps.sources.etools',
    'etools_datamart.apps.sources.source_prp.apps.Config',

    'etools_datamart.apps.mart.data',
    'etools_datamart.apps.mart.rapidpro',
    'etools_datamart.apps.mart.prp',

    'etools_datamart.api',
    'impersonate',
    'admin_extra_urls',
    'adminactions',

    'jsoneditor',

    'explorer',
    'unicef_rest_framework.apps.Config',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    'unicef_security',
    # 'redisboard',
    'django_filters',
    'month_field',
    'drf_querystringfilter',
    'crispy_forms',
    'drf_yasg',
    'adminfilters',
    'post_office',
    'djcelery_email',
    'django_celery_beat',
    'django_extensions',

]
DATE_FORMAT = '%d %b %Y'
DATE_INPUT_FORMATS = [
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',  # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',  # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
]

DATETIME_FORMAT = '%d %b %Y %H:%M:%S'

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
EMAIL_BACKEND = 'post_office.backends.EmailBackend'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_SUBJECT_PREFIX = "[ETOOLS-DATAMART]"
POST_OFFICE = {
    'DEFAULT_PRIORITY': 'now',
    'BACKENDS': {
        'default': 'djcelery_email.backends.CeleryEmailBackend'
    }
}

# crispy-forms
CRISPY_FAIL_SILENTLY = not DEBUG
CRISPY_CLASS_CONVERTERS = {'textinput': "textinput inputtext"}
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# django-secure
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE')

SECURE_BROWSER_XSS_FILTER = env.bool('SECURE_BROWSER_XSS_FILTER')
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('SECURE_CONTENT_TYPE_NOSNIFF')
SECURE_FRAME_DENY = env.bool('SECURE_FRAME_DENY')
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD')
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_HTTPONLY = env.bool('SESSION_COOKIE_HTTPONLY')
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE')
X_FRAME_OPTIONS = env('X_FRAME_OPTIONS')
USE_X_FORWARDED_HOST = env('USE_X_FORWARDED_HOST')
SESSION_SAVE_EVERY_REQUEST = True
NOTIFICATION_SENDER = "etools_datamart@unicef.org"

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
    'ETOOLS_ADDRESS': ('https://etools.unicef.org', 'eTools hostname', str),
    'RAPIDPRO_ADDRESS': ('https://app.rapidpro.io/', 'RapidPro default hostname', str),
    'CACHE_VERSION': (1, 'Global cache version', int),
    'CACHE_ENABLED': (True, 'Enable/Disable API cache', bool),
    'AZURE_USE_GRAPH': (True, 'Use MS Graph API to fetch user data', bool),
    'DEFAULT_GROUP': ('Guests', 'Default group new users belong to', 'select_group'),
    'ANALYTICS_CODE': (env('ANALYTICS_CODE'), 'Google analytics code'),
    'DISABLE_SCHEMA_RESTRICTIONS': (env('DISABLE_SCHEMA_RESTRICTIONS'), 'Disable per user schema authorizations'),
    'DISABLE_SERVICE_RESTRICTIONS': (env('DISABLE_SERVICE_RESTRICTIONS'), 'Disable per user service authorizations'),

    'ETL_MAX_RETRIES': (30, 'Max retries for dependent tasks', int),
    'ETL_RETRY_COUNTDOWN': (180, 'Retry counddown in secods', int),
    'ALLOW_EMAIL_PASSWORD': (False, 'Allow send local password by email', bool)

}

CELERY_ACCEPT_CONTENT = ['etljson']
CELERY_BEAT_SCHEDULER = env.str(
    'CELERY_BEAT_SCHEDULER',
    default='unicef_rest_framework.schedulers:DatabaseScheduler',
)
CELERY_BROKER_POOL_LIMIT = env.int('CELERY_BROKER_POOL_LIMIT', default=0)
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_EAGER_PROPAGATES_EXCEPTIONS = env.bool('CELERY_ALWAYS_EAGER')
CELERY_REDIS_MAX_CONNECTIONS = env.int('CELERY_REDIS_MAX_CONNECTIONS', 10)
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_RESULT_SERIALIZER = 'etljson'
CELERY_TASK_ALWAYS_EAGER = env.bool('CELERY_TASK_ALWAYS_EAGER')
CELERY_TASK_SERIALIZER = 'etljson'
CELERY_TIMEZONE = TIME_ZONE
CELERY_EMAIL_TASK_CONFIG = {
    'queue' : 'mail',
}

CELERY_EMAIL_BACKEND = env.str(
    'CELERY_EMAIL_BACKEND',
    default='post_office.backends.EmailBackend',
)
CELERY_EMAIL_CHUNK_SIZE = 10
EXPORT_NOTIFICATIONS_ENABLED = env.bool(
    'EXPORT_NOTIFICATIONS_ENABLED',
    default=True,
)

CONCURRENCY_IGNORE_DEFAULT = False

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "PAGE_SIZE": 100,
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'unicef_rest_framework.negotiation.CT',
    'DEFAULT_PAGINATION_CLASS': 'unicef_rest_framework.pagination.APIPagination',
    'DEFAULT_METADATA_CLASS': 'etools_datamart.api.metadata.SimpleMetadataWithFilters',
    'DEFAULT_VERSIONING_CLASS': 'unicef_rest_framework.versioning.URFVersioning',
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
    'DATETIME_FORMAT': DATETIME_FORMAT,
    # 'DATE_FORMAT': DATE_FORMAT,
    'DEFAULT_SCHEMA_CLASS': 'etools_datamart.api.endpoints.openapi.DatamartAutoSchema',

}

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
    'JWT_PUBLIC_KEY': '?',
    # 'JWT_PRIVATE_KEY': wallet.get_private(),
    # 'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'RS256',

}
# django-sql-explorer
EXPLORER_CONNECTIONS = {'Default': 'default',
                        'eTools': 'etools'}
EXPLORER_DEFAULT_CONNECTION = 'default'
EXPLORER_ASYNC_SCHEMA = True
EXPLORER_CONNECTION_NAME = 'default'
EXPLORER_PERMISSION_VIEW = lambda u: u.is_superuser
EXPLORER_PERMISSION_CHANGE = lambda u: u.is_superuser
EXPLORER_TOKEN = env('EXPLORER_TOKEN')
EXPLORER_FROM_EMAIL = 'datamart@unicef.io'
# social auth
# WARNINGS: UNICEF pipeline does not work if other provider
# are added to UNICEF AD. Dio not change below settings
#
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = False
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['username']
SOCIAL_AUTH_SANITIZE_REDIRECTS = False
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_WHITELISTED_DOMAINS = ['unicef.org', ]
SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT = True
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'unicef_security.graph.get_unicef_user',
    # 'unicef_security.azure.social_uid',
    # 'social_core.pipeline.social_auth.social_uid',
    # 'social_core.pipeline.social_auth.social_user',
    # 'social_core.pipeline.user.get_username',
    # 'social_core.pipeline.user.create_user',
    # 'unicef_security.azure.get_username',
    # 'unicef_security.azure.create_user',
    # 'social_core.pipeline.social_auth.associate_user',
    # 'social_core.pipeline.social_auth.load_extra_data',
    # 'social_core.pipeline.user.user_details',
    # 'social_core.pipeline.social_auth.associate_by_email',
    'unicef_security.graph.default_group',
)

SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = env.str('AZURE_CLIENT_ID')
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = env.str('AZURE_CLIENT_SECRET')
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = env.str('AZURE_TENANT')
SOCIAL_AUTH_AZUREAD_OAUTH2_KEY = env.str('AZURE_CLIENT_ID')
SOCIAL_AUTH_AZUREAD_OAUTH2_RESOURCE = 'https://graph.microsoft.com/'
SOCIAL_AUTH_USER_MODEL = 'unicef_security.User'

# POLICY = os.getenv('AZURE_B2C_POLICY_NAME', "b2c_1A_UNICEF_PARTNERS_signup_signin")
SCOPE = ['openid', ]
IGNORE_DEFAULT_SCOPE = True

SWAGGER_SETTINGS = {
    'DEFAULT_API_URL': env('ABSOLUTE_BASE_URL') + env('API_PREFIX'),
    # 'DEFAULT_AUTO_SCHEMA_CLASS': 'etools_datamart.api.swagger.schema.APIAutoSchema',
    # 'DEFAULT_FILTER_INSPECTORS': ['etools_datamart.api.swagger.filters.APIFilterInspector', ],
    'DISPLAY_OPERATION_ID': False,
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
            'format': '%(levelname)-8s: %(asctime)s %(name)20s: %(funcName)s:%(lineno)s %(message)s'
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
        'drf_querystringfilter': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': False
        },
        'unicef_rest_framework': {
            'handlers': ['console', ],
            'level': 'ERROR',
            'propagate': False
        },
        'etools_datamart': {
            'handlers': ['null', ],
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
SCHEMA_EXCLUDE = {'schema_name__in': env.list('IGNORED_SCHEMAS')}

ENABLE_LIVE_STATS = env('ENABLE_LIVE_STATS')

BUSINESSAREA_MODEL = 'unicef_security.BusinessArea'
AUTH_USER_MODEL = 'unicef_security.User'


def extra(r):
    return {'AZURE_CLIENT_ID': os.environ['AZURE_CLIENT_ID'],
            'GRAPH_CLIENT_ID': os.environ['GRAPH_CLIENT_ID'],
            'AZURE_TENANT': os.environ['AZURE_TENANT']}


SYSINFO = {"extra": {'Azure': extra}}

MIGRATION_MODULES = {'explorer': 'etools_datamart.custom_migrations.explorer', }

IMPERSONATE = {
    'PAGINATE_COUNT': 50,
    'REQUIRE_SUPERUSER': True,
    'CUSTOM_USER_QUERYSET': 'etools_datamart.libs.impersonate.queryset'
}

SENTRY_ENABLED = env.bool('SENTRY_ENABLED', False)
SENTRY_DSN = env('SENTRY_DSN', '')

if SENTRY_ENABLED:
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration

    # from sentry_sdk.integrations.redis import RedisIntegration

    sentry_sdk.init(dsn=SENTRY_DSN,
                    integrations=[DjangoIntegration(), CeleryIntegration()],
                    release=get_full_version(),
                    debug=False)

    def before_send(event, hint):
        from django.core.exceptions import ObjectDoesNotExist
        if 'exc_info' in hint:
            exc_type, exc_value, tb = hint['exc_info']
            if isinstance(exc_value, SMTPServerDisconnected):
                return None
            elif isinstance(exc_value, KeyError):
                return None
            elif isinstance(exc_value, ObjectDoesNotExist):
                if 'rapidpro' in event.get('tags', {}).get('loader', ''):
                    return None
            elif isinstance(exc_value, AttributeError) and str(exc_value) == "'Run' object has no attribute 'source_id'":
                return None
            event['tags']['stack'] = env('STACK')
        return event

    sentry_sdk.init(before_send=before_send)

SILENCED_SYSTEM_CHECKS = ["models.E006", "models.E007"]

FORMAT_MODULE_PATH = 'etools_datamart.locale'

EXPORT_FILE_STORAGE = env('EXPORT_FILE_STORAGE')
EXPORT_FILE_STORAGE_KWARGS = env('EXPORT_FILE_STORAGE_KWARGS')

AZURE_ACCOUNT_NAME = env('AZURE_STORAGE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = env('AZURE_STORAGE_ACCOUNT_KEY')
AZURE_OVERWRITE_FILES = env('AZURE_STORAGE_OVERWRITE_FILES')
AZURE_CONTAINER = env('AZURE_STORAGE_CONTAINER')
AZURE_LOCATION = env('AZURE_STORAGE_LOCATION')
AZURE_AUTO_SIGN = env('AZURE_STORAGE_AUTO_SIGN')
AZURE_ACCESS_MODE = env('AZURE_STORAGE_ACCESS_MODE')
AZURE_ACCESS_TTL = env('AZURE_STORAGE_ACCESS_TTL')

REQUEST_TIMEOUT = env('REQUEST_TIMEOUT')
GEONAMES_URL = env('GEONAMES_URL')
GEONAMES_USERNAME = env('GEONAMES_USERNAME')

# FIELD_SIZE_LIMIT = 32000
