import os
import sys
import warnings

import psycopg2
import pytest
from _pytest.deprecated import RemovedInPytest4Warning
from django.db import connections
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def pytest_configure(config):
    here = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(here, 'extras'))
    # enable this to remove deprecations
    warnings.simplefilter('once', DeprecationWarning)
    warnings.simplefilter('ignore', RemovedInPytest4Warning)

    # os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


@pytest.fixture(autouse=True)
def configure_test(settings):
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',

    ]
    settings.AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )
    settings.SECURE_SSL_REDIRECT = False


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
    # never touch etools DB
    from pytest_django.fixtures import django_db_setup as dj_db_setup
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
