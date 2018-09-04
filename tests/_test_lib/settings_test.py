from etools_datamart.config.settings import *  # noqa

CACHES['api']['BACKEND'] = "django.core.cache.backends.dummy.DummyCache"  # noqa

# Use only one db during tests
DATABASES['etools']['PORT'] = DATABASES['default']['PORT']  # noqa
DATABASES['etools']['HOST'] = DATABASES['default']['HOST']  # noqa
DATABASES['etools']['USERNAME'] = DATABASES['default'].get('USERNAME', "")  # noqa
DATABASES['etools']['PASSWORD'] = DATABASES['default'].get('PASSWORD', "")  # noqa

TEST_SCHEMAS = ['bolivia', 'chad', 'lebanon']
SCHEMA_FILTER = {'schema_name__in': TEST_SCHEMAS}
SCHEMA_EXCLUDE = {}

CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_FRAME_DENY = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_SECONDS = 1
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_HTTPONLY = False
ALLOWED_HOSTS = ['*']
STATIC_ROOT = os.path.dirname(__file__)  # noqa
SESSION_COOKIE_SECURE = False
