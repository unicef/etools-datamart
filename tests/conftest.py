import warnings
from unittest.mock import Mock

import pytest
from _pytest.deprecated import RemovedInPytest4Warning
from _pytest.fixtures import SubRequest
from test_utilities.factories import UserFactory


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
    from etools_datamart.apps.tracking.models import APIRequestLog

    with django_db_blocker.unblock():
        Service.objects.load_services()
        UserAccessControl.objects.all().delete()
        APIRequestLog.objects.truncate()
        UserFactory(username='system', is_superuser=True)
        assert Service.objects.exists()
        assert not APIRequestLog.objects.exists()


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

    state.request = None
    conn = connections['etools']
    conn.search_path = None


@pytest.fixture(autouse=True)
def disable_stats(request: SubRequest, monkeypatch):
    if 'enable_threadstats' in request.funcargnames:
        pass
    elif 'enable_stats' in request.funcargnames:
        from etools_datamart.apps.tracking.middleware import StatsMiddleware
        monkeypatch.setattr('etools_datamart.apps.tracking.middleware.ThreadedStatsMiddleware.log',
                            StatsMiddleware.log
                            )

    else:
        monkeypatch.setattr('etools_datamart.apps.tracking.middleware.ThreadedStatsMiddleware.log',
                            Mock())


@pytest.fixture()
def enable_stats(request):
    pass


@pytest.fixture()
def enable_threadstats(request):
    pass


@pytest.fixture()
def service(db):
    from unicef_rest_framework.models import Service
    service = Service.objects.order_by('?').first()
    if not service:
        Service.objects.load_services()
        service = Service.objects.order_by('?').first()
    return service


@pytest.fixture()
def data_service(db):
    from etools_datamart.api.endpoints import InterventionViewSet

    return InterventionViewSet.get_service()


# Change below numbers each time etools dump is updated

@pytest.fixture()
def number_of_partnerorganization(db):
    # number of partners.PartnerOrganization records in each tenant
    return 193


@pytest.fixture()
def number_of_intervention(db):
    return 3
