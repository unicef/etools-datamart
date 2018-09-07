import warnings

import pytest
from _pytest.deprecated import RemovedInPytest4Warning


def pytest_configure(config):
    # enable this to remove deprecations
    warnings.simplefilter('once', DeprecationWarning)
    warnings.simplefilter('ignore', RemovedInPytest4Warning)


#
# @pytest.fixture(autouse=True)
# def configure_test(settings, monkeypatch):
#
#     from etools_datamart.config.settings import env
#     settings.DATABASES['default'] = env.db()
#     settings.DATABASES['etools'] = env.db('DATABASE_URL_ETOOLS', engine='etools_datamart.apps.multitenant.postgresql')
#     settings.CSRF_COOKIE_SECURE = False
#     settings.SECURE_BROWSER_XSS_FILTER = False
#     settings.SECURE_CONTENT_TYPE_NOSNIFF = False
#     settings.SECURE_FRAME_DENY = False
#     settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = False
#     settings.SECURE_HSTS_SECONDS = 1
#     settings.SECURE_SSL_REDIRECT = False
#     settings.SESSION_COOKIE_HTTPONLY = False
#     settings.ALLOWED_HOSTS = ['*']
#     settings.STATIC_ROOT = str(Path(__file__).parent)
#     settings.SESSION_COOKIE_SECURE = False
#     settings.CACHES['api']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
#     # settings.CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
#     settings.TEST_SCHEMAS = ['bolivia', 'chad', 'lebanon']
#     settings.SCHEMA_FILTER = {'schema_name__in': settings.TEST_SCHEMAS}
#     settings.SCHEMA_EXCLUDE = {}


#
#
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

    from unicef_rest_framework.models import Service, UserAccessControl
    with django_db_blocker.unblock():
        Service.objects.load_services()
        UserAccessControl.objects.all().delete()


@pytest.fixture
def user1(db):
    from test_utilities.factories import UserFactory
    return UserFactory()


@pytest.fixture
def user2(db):
    from test_utilities.factories import UserFactory
    return UserFactory()


@pytest.fixture(autouse=True)
def reset(monkeypatch):
    from etools_datamart.state import state
    from django.db import connections

    # if 'valid' in state.schemas.__dict__:
    #     del state.schemas.valid

    state.request = None
    conn = connections['etools']
    conn.search_path = None
