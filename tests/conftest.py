import os
import sys
import tempfile
import uuid
import warnings
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from _pytest.fixtures import SubRequest

from etools_datamart.apps.etl.models import EtlTask


def pytest_configure(config):
    # enable this to remove deprecations
    os.environ['CELERY_TASK_ALWAYS_EAGER'] = "1"
    os.environ['STATIC_ROOT'] = tempfile.gettempdir()


# warnings.simplefilter('once', DeprecationWarning)
# warnings.simplefilter('ignore', RemovedInPytest4Warning)
# warnings.simplefilter('ignore', PendingDeprecationWarning)
warnings.simplefilter('ignore', UserWarning)


@pytest.fixture(scope="session")
def disable_migration_signals(request):
    return request.config.option.disable_migration_signals
    # FIXME: pdb
    # import pdb; pdb.set_trace()
    # if 'disable_migration_signals' in request.config.items():
    #     return request.config.getvalue("disable_migration_signals")
    #
    # return request.config.inicfg.get('disable_migration_signals') == 'true'


def pytest_addoption(parser):
    group = parser.getgroup("django")
    group._addoption(
        "--disable-migration-signals",
        action="store_true",
        dest="disable_migration_signals",
        default=False,
        help="disable pre/post migration signals",
    )


@pytest.yield_fixture(scope='session')
def django_db_setup(request,
                    django_test_environment,
                    django_db_blocker,
                    django_db_use_migrations,
                    django_db_keepdb,
                    django_db_createdb,
                    django_db_modify_db_settings,
                    disable_migration_signals):
    if not django_db_createdb and django_db_keepdb and disable_migration_signals:
        sys.stdout.write("Warning pre/post migrate signals have been dosabled\n")
        import django.core.management.commands.migrate
        django.core.management.commands.migrate.emit_pre_migrate_signal = MagicMock()
        django.core.management.commands.migrate.emit_post_migrate_signal = MagicMock()
    #
    # from pytest_django.fixtures import django_db_setup as dj_db_setup
    # dj_db_setup(request,
    #             django_test_environment,
    #             django_db_blocker,
    #             django_db_use_migrations,
    #             django_db_keepdb,
    #             django_db_createdb,
    #             django_db_modify_db_settings)

    """Top level fixture to ensure test databases are available"""
    from pytest_django.compat import setup_databases, teardown_databases
    from pytest_django.fixtures import _disable_native_migrations
    setup_databases_args = {}

    if not django_db_use_migrations:
        _disable_native_migrations()

    if django_db_keepdb and not django_db_createdb:
        setup_databases_args["keepdb"] = True

    with django_db_blocker.unblock():
        db_cfg = setup_databases(
            verbosity=pytest.config.option.verbose,
            interactive=False,
            **setup_databases_args
        )

    def teardown_database():
        with django_db_blocker.unblock():
            teardown_databases(db_cfg, verbosity=pytest.config.option.verbose)

    if not django_db_keepdb:
        request.addfinalizer(teardown_database)

    #
    from unicef_rest_framework.models import Service, UserAccessControl
    from etools_datamart.apps.tracking.models import APIRequestLog
    from test_utilities.factories import UserFactory
    with django_db_blocker.unblock():
        EtlTask.objects.inspect()
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
    # from etools_datamart.state import state
    from django.db import connections
    monkeypatch.setattr("etools_datamart.apps.security.utils.cache", MagicMock(get=lambda *a: []))
    # state.request = None
    conn = connections['etools']
    conn.set_schemas([])
    conn.search_path = None


@pytest.fixture(autouse=True)
def disable_stats(request: SubRequest, monkeypatch):
    pass  # FIXME: ThreadedStatsMiddleware has some side effects in test..
    # if 'enable_threadstats' in request.funcargnames:
    #     pass
    # elif 'enable_stats' in request.funcargnames:
    #     from etools_datamart.apps.tracking.middleware import StatsMiddleware
    #     monkeypatch.setattr('etools_datamart.apps.tracking.middleware.ThreadedStatsMiddleware.log',
    #                         StatsMiddleware.log
    #                         )
    #
    # else:
    #     monkeypatch.setattr('etools_datamart.apps.tracking.middleware.ThreadedStatsMiddleware.log',
    #                         Mock())


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


# Check below numbers each time etools dump is updated
# Should be automatically updated by 'db/update_etools_schema.sh'
@pytest.fixture()
def number_of_partnerorganization(db):
    # number of partners.PartnerOrganization records in each tenant
    return int((Path(__file__).parent / 'PARTNERORGANIZATION').read_text())


@pytest.fixture()
def number_of_intervention(db):
    # number of partners.Intervention
    return int((Path(__file__).parent / 'INTERVENTION').read_text())


@pytest.fixture()
def etools_user(db):
    from etools_datamart.apps.etools.models import AuthUser
    return AuthUser.objects.get(id=1)


@pytest.fixture()
def staff_user(etools_user):
    from test_utilities.factories import UserFactory
    return UserFactory(username=etools_user.username,
                       email=etools_user.email,
                       is_staff=True)


@pytest.fixture()
def user(etools_user):
    from test_utilities.factories import UserFactory

    return UserFactory(username=etools_user.username,
                       azure_id=uuid.uuid4(),
                       email=etools_user.email)


@pytest.fixture()
def local_user(db):
    from test_utilities.factories import UserFactory

    return UserFactory()
