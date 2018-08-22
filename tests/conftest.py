import os
import sys
import warnings
from pathlib import Path

import psycopg2
import pytest
from _pytest.deprecated import RemovedInPytest4Warning
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def pytest_configure(config):
    here = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(here, 'extras'))
    # enable this to remove deprecations
    warnings.simplefilter('once', DeprecationWarning)
    warnings.simplefilter('ignore', RemovedInPytest4Warning)

    os.environ['CSRF_COOKIE_SECURE'] = "0"
    os.environ['SECURE_SSL_REDIRECT'] = "0"
    os.environ['SESSION_COOKIE_SECURE'] = "0"
    # os.environ['DATABASE_URL'] = "postgres://postgres:@127.0.0.1:5432/etools_datamart"
    # os.environ['DATABASE_URL_ETOOLS'] = "postgis://postgres:@127.0.0.1:5432/etools"
    # from etools_datamart.config import settings
    # settings.DATABASES['etools']['HOST'] = '127.0.0.1'
    # settings.DATABASES['etools']['PORT'] = '5432'


@pytest.fixture(autouse=True)
def configure_test(settings):
    from etools_datamart.config.settings import env
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',

    ]
    settings.AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )
    settings.DATABASES['default'] = env.db()
    settings.DATABASES['etools'] = env.db('DATABASE_URL_ETOOLS', engine='etools_datamart.apps.multitenant.postgresql')
    settings.CSRF_COOKIE_SECURE = False
    settings.SECURE_BROWSER_XSS_FILTER = False
    settings.SECURE_CONTENT_TYPE_NOSNIFF = False
    settings.SECURE_FRAME_DENY = False
    settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    settings.SECURE_HSTS_SECONDS = 1
    settings.SECURE_SSL_REDIRECT = False
    settings.SESSION_COOKIE_HTTPONLY = False
    settings.ALLOWED_HOSTS = ['*']
    settings.STATIC_ROOT = str(Path(__file__).parent)
    settings.SESSION_COOKIE_SECURE = False


@pytest.yield_fixture(scope='session')
def django_db_setup(request,
                    django_test_environment,
                    django_db_blocker,
                    django_db_use_migrations,
                    django_db_keepdb,
                    django_db_createdb,
                    django_db_modify_db_settings):
    # never touch etools DB
    from pytest_django.fixtures import django_db_setup as dj_db_setup, _disable_native_migrations
    from pytest_django.compat import teardown_databases
    from django.test.utils import setup_databases
    return
    setup_databases_args = {}
    if not django_db_use_migrations:
        _disable_native_migrations()

    if django_db_keepdb and not django_db_createdb:
        setup_databases_args['keepdb'] = True

    with django_db_blocker.unblock():
        db_cfg = setup_databases(
            verbosity=pytest.config.option.verbose,
            interactive=False,
            **setup_databases_args
        )

    def teardown_database():
        with django_db_blocker.unblock():
            teardown_databases(
                db_cfg,
                verbosity=pytest.config.option.verbose,
            )

    if not django_db_keepdb:
        request.addfinalizer(teardown_database)


@pytest.fixture
def user1(db):
    from test_utils.factories import UserFactory
    return UserFactory()


@pytest.fixture(autouse=True)
def reset():
    from etools_datamart.state import state
    from django.db import connections

    state.schema = []
    state.request = None
    conn = connections['etools']
    conn.clear_search_paths()


@pytest.fixture()
def bolivia():
    from etools_datamart.state import state
    state.schema = ['bolivia']
