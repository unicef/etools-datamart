import os
import random

from etools_datamart.config.settings import *  # noqa

SEED = random.random()


def cache_random_prefix(*args, **kwargs):
    return str(SEED)


# CACHES['default']['BACKEND'] = "django.core.cache.backends.dummy.DummyCache"  # noqa
CACHES['api']['BACKEND'] = "django.core.cache.backends.dummy.DummyCache"  # noqa
# CACHES['lock']['BACKEND'] = "django.core.cache.backends.dummy.DummyCache"  # noqa

CACHES['locmem'] = {  # noqa
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'LOCATION': 'unique-snowflake',
}

CACHES['redis'] = env.cache('CACHE_URL')  # noqa
# we must have redis here to check for pickling errors
assert CACHES['redis']['BACKEND'] == 'django_redis.cache.RedisCache'  # noqa
assert CACHES['lock']['BACKEND'] == 'django_redis.cache.RedisCache'  # noqa

CACHES['api']['KEY_FUNCTION'] = cache_random_prefix  # noqa
CACHES['default']['KEY_FUNCTION'] = cache_random_prefix  # noqa

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

LOGGING['loggers']['etools_datamart']['handlers'] = ['null']  # noqa
LOGGING['loggers']['']['handlers'] = ['null']  # noqa
LOGGING['loggers']['unicef_rest_framework']['handlers'] = ['null']  # noqa
