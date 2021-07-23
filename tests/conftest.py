import os
import sys
import tempfile
import uuid
import warnings
from pathlib import Path
from unittest.mock import MagicMock

# def _setup_models():
#     from django.db import connection
#     from django.db.backends.utils import truncate_name
#     from django.db.models import Model
#
#     from django.conf import settings
#     # settings.DATABASE_ROUTERS = []
#     #
#     # from django.apps import apps
#     # from etools_datamart.apps.core.readonly import ReadOnlyModel
#     # for m in apps.get_models():
#     #     if m._meta.proxy:
#     #         opts = m._meta.proxy_for_model._meta
#     #     else:
#     #         opts = m._meta
#     #
#     #     if opts.app_label not in ('contenttypes', 'sites'):
#     #         db_table = ('{0.app_label}_{0.model_name}'.format(opts)).lower()
#     #         m._meta.db_table = truncate_name(db_table, connection.ops.max_name_length())
#     #         m._meta.db_tablespace = ''
#     #
#     #     if not m._meta.managed:
#     #         m._meta.managed = True
#     #
#     #     if issubclass(m, ReadOnlyModel):
#     #         setattr(m, 'save', Model.save)
from django.db.models import signals

import pytest
from _pytest.fixtures import SubRequest


def pytest_configure(config):
    # enable this to remove deprecations
    os.environ['CELERY_TASK_ALWAYS_EAGER'] = "1"
    os.environ['STATIC_ROOT'] = tempfile.gettempdir()
    sys._called_from_pytest = True
    # if not config.option.help:
    #     _setup_models()


def pytest_unconfigure(config):
    import sys
    del sys._called_from_pytest


# warnings.simplefilter('once', DeprecationWarning)
# warnings.simplefilter('ignore', RemovedInPytest4Warning)
# warnings.simplefilter('ignore', PendingDeprecationWarning)
# warnings.simplefilter('ignore', UserWarning)
warnings.simplefilter('ignore', RuntimeWarning, lineno=1421)


@pytest.fixture(scope="session")
def enable_migration_signals(request):
    return request.config.option.enable_migration_signals


def pytest_addoption(parser):
    group = parser.getgroup("django")
    group._addoption(
        "--enable-migration-signals",
        action="store_true",
        dest="enable_migration_signals",
        default=False,
        help="re-enable pre/post migration signals",
    )
    group._addoption(
        "--record-new-urls",
        action="store_true",
        dest="record_new_urls",
        default=False,
        help="",
    )


@pytest.fixture(scope='session')
def django_db_setup(request,
                    django_test_environment,
                    django_db_blocker,
                    django_db_use_migrations,
                    django_db_keepdb,
                    django_db_createdb,
                    django_db_modify_db_settings,
                    enable_migration_signals,
                    pytestconfig):
    if django_db_createdb or enable_migration_signals:
        warnings.warn("Warning: pre/post migrate signals are enabled \n")
    else:
        warnings.warn("Warning: pre/post migrate signals have been disabled\n")
        import django.core.management.commands.migrate
        django.core.management.commands.migrate.emit_pre_migrate_signal = MagicMock()
        django.core.management.commands.migrate.emit_post_migrate_signal = MagicMock()

    # """Top level fixture to ensure test databases are available"""
    from django.test.utils import setup_databases, teardown_databases

    from pytest_django.fixtures import _disable_native_migrations
    setup_databases_args = {}

    if not django_db_use_migrations:
        _disable_native_migrations()

    if django_db_keepdb and not django_db_createdb:
        setup_databases_args["keepdb"] = True
    # this patch is logically wrong, but we do not use constance permissions
    # otherwise test fails with
    #
    # .venv/lib/python3.9/site-packages/django/db/backends/utils.py:84: in _execute
    #     return self.cursor.execute(sql, params)
    # E   django.db.utils.ProgrammingError: relation "django_content_type" does not exist
    # E   LINE 1: ..."."app_label", "django_content_type"."model" FROM "django_co...
    # E                                                                ^
    #
    signals.post_migrate.disconnect(dispatch_uid='constance.create_perm')
    with django_db_blocker.unblock():
        db_cfg = setup_databases(
            verbosity=request.config.option.verbose,
            interactive=False,
            **setup_databases_args
        )

    def _teardown_database():
        with django_db_blocker.unblock():
            teardown_databases(db_cfg, verbosity=request.config.option.verbose)

    if not django_db_keepdb:
        request.addfinalizer(_teardown_database)

    from test_utilities.factories import UserFactory

    from unicef_rest_framework.models import Service, UserAccessControl

    from etools_datamart.apps.etl.models import EtlTask
    from etools_datamart.apps.tracking.models import APIRequestLog

    with django_db_blocker.unblock():
        EtlTask.objects.inspect()
        Service.objects.load_services()
        UserAccessControl.objects.all().delete()
        APIRequestLog.objects.truncate()
        UserFactory(username='system', is_superuser=True)
        from django.contrib.sites.models import Site
        Site.objects.get_or_create(domain='example.com', name='example.com')
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
    return int((Path(__file__).parent / 'COUNT_PARTNERS_PARTNERORGANIZATION').read_text())


@pytest.fixture()
def number_of_intervention(db):
    # number of partners.Intervention
    return int((Path(__file__).parent / 'COUNT_PARTNERS_INTERVENTION').read_text())


@pytest.fixture()
def etools_user(db):
    from etools_datamart.apps.sources.etools.models import AuthUser
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


@pytest.fixture()
def schema_access_control(db):
    from test_utilities.factories import SchemaAccessControlFactory

    return SchemaAccessControlFactory()
