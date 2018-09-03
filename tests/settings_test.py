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
