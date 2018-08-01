import os
import sys
import warnings

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


@pytest.fixture(autouse=True)
def configure_test(settings):
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',

    ]
    settings.AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )
    settings.CSRF_COOKIE_SECURE = False
    settings.SECURE_BROWSER_XSS_FILTER = False
    settings.SECURE_CONTENT_TYPE_NOSNIFF = False
    settings.SECURE_FRAME_DENY = False
    settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    settings.SECURE_HSTS_SECONDS = 1
    settings.SECURE_SSL_REDIRECT = False
    settings.SESSION_COOKIE_HTTPONLY = False
    settings.ALLOWED_HOSTS = ['*']
    settings.SESSION_COOKIE_SECURE = False


def run_sql(sql):
    conn = psycopg2.connect(database='postgres')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.yield_fixture(scope='session')
def django_db_setup(request,
                    django_test_environment,
                    django_db_blocker,
                    django_db_use_migrations,
                    django_db_keepdb,
                    django_db_createdb,
                    django_db_modify_db_settings):
    pass
    # never touch etools DB
    # from pytest_django.fixtures import django_db_setup as dj_db_setup
    # dj_db_setup(request,
    #             django_test_environment,
    #             django_db_blocker,
    #             django_db_use_migrations,
    #             django_db_keepdb,
    #             django_db_createdb,
    #             django_db_modify_db_settings)
    #
    #
    # from django.conf import settings
    # settings.DATABASES['etools']['NAME'] = 'etools'
    # settings.DATABASES['etools']['TEST']['NAME'] = 'etools'


@pytest.fixture
def user1(db):
    from test_utils.factories import UserFactory
    return UserFactory()
