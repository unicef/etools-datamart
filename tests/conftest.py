import os
import sys
import warnings
import pytest
from _pytest.deprecated import RemovedInPytest4Warning


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


@pytest.fixture
def user1(db):
    from test_utils.factories import UserFactory
    return UserFactory()
