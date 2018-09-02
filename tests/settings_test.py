from etools_datamart.config.settings import *  # noqa

CACHES['api']['BACKEND'] = "django.core.cache.backends.dummy.DummyCache"  # noqa
