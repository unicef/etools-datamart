import os
import sys
import warnings
from pathlib import Path

import pytest
from _pytest.deprecated import RemovedInPytest4Warning


def pytest_configure(config):
    here = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(here, 'extras'))
    # enable this to remove deprecations
    warnings.simplefilter('once', DeprecationWarning)
    warnings.simplefilter('ignore', RemovedInPytest4Warning)

    # os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_test'
    os.environ['ENV_FILE_PATH'] = os.path.abspath(os.path.dirname(__file__))
    os.environ['CSRF_COOKIE_SECURE'] = "0"
    os.environ['SECURE_SSL_REDIRECT'] = "0"
    os.environ['SESSION_COOKIE_SECURE'] = "0"
    os.environ['API_CACHE_URL'] = "dummycache://"
    # import django
    # django.setup()
    # os.environ['DATABASE_URL'] = "postgres://postgres:@127.0.0.1:5432/etools_datamart"
    # os.environ['DATABASE_URL_ETOOLS'] = "postgis://postgres:@127.0.0.1:5432/etools"
    # from etools_datamart.config import settings
    # settings.DATABASES['etools']['HOST'] = '127.0.0.1'
    # settings.DATABASES['etools']['PORT'] = '5432'
    # import django.core.cache
    # from django.core.cache import CacheHandler
    # django.core.cache.caches = CacheHandler()


@pytest.fixture(autouse=True)
def configure_test(settings, monkeypatch):
    # from etools_datamart.config.settings import env
    # settings.DATABASES['default'] = env.db()
    # settings.DATABASES['etools'] = env.db('DATABASE_URL_ETOOLS', engine='etools_datamart.apps.multitenant.postgresql')
    # settings.CSRF_COOKIE_SECURE = False
    # settings.SECURE_BROWSER_XSS_FILTER = False
    # settings.SECURE_CONTENT_TYPE_NOSNIFF = False
    # settings.SECURE_FRAME_DENY = False
    # settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    # settings.SECURE_HSTS_SECONDS = 1
    # settings.SECURE_SSL_REDIRECT = False
    # settings.SESSION_COOKIE_HTTPONLY = False
    # settings.ALLOWED_HOSTS = ['*']
    settings.STATIC_ROOT = str(Path(__file__).parent)
    # settings.SESSION_COOKIE_SECURE = False
    settings.CACHES['api']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
    settings.CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
    #


@pytest.yield_fixture(scope='session')
def django_db_setup(request,
                    django_test_environment,
                    django_db_blocker,
                    django_db_use_migrations,
                    django_db_keepdb,
                    django_db_createdb,
                    django_db_modify_db_settings):
    # never touch etools DB
    from pytest_django.fixtures import django_db_setup as dj_db_setup
    dj_db_setup(request,
                django_test_environment,
                django_db_blocker,
                django_db_use_migrations,
                django_db_keepdb,
                django_db_createdb,
                django_db_modify_db_settings)

    from unicef_rest_framework.models import Service
    with django_db_blocker.unblock():
        Service.objects.load_services()


@pytest.fixture
def user1(db):
    from test_utilities.factories import UserFactory
    return UserFactory()


@pytest.fixture(autouse=True)
def reset(monkeypatch):
    # def get_tenants():
    #     return UsersCountry.objects.filter(schema_name__in=settings.TEST_SCHEMAS).order_by('name')

    # from etools_datamart.apps.etools.models import UsersCountry
    # from django.conf import settings
    from etools_datamart.state import state

    # monkeypatch.setattr('etools_datamart.apps.multitenant.postgresql.base.DatabaseWrapper.get_tenants',
    #                     lambda s: settings.TEST_SCHEMAS)

    from django.db import connections
    # conn = connections['etools']
    # conn.get_tenants = get_tenants

    if 'valid' in state.schemas.__dict__:
        del state.schemas.valid

    state.request = None
    conn = connections['etools']
    conn.search_path = None
