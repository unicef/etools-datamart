import time
from io import StringIO
from unittest import mock

import pytest
from strategy_field.utils import fqn

from etools_datamart.apps.etl.exceptions import RequiredIsMissing, RequiredIsRunning
from etools_datamart.apps.etl.loader import EtlResult
from etools_datamart.apps.mart.data.models import ActionPoint, Partner


@pytest.fixture()
def loader1(db):
    loader = ActionPoint.loader
    loader.config.lock_key = str(time.time())
    return loader


def test_load_requiredismissing(loader1):
    # with mock.patch("etools_datamart.apps.mart.data.models.Intervention.loader.check_refresh", lambda *a: True):
    # update_context() is mocked only to prevent not needed long-running test
    # because update_context() is invoked only if RequiredIsMissing is not raised
    # we do not want to wait the full load only to detect the error
    with mock.patch(
        "%s.update_context" % fqn(loader1), side_effect=Exception("missing to raise RequiredIsMissing")
    ):
        with pytest.raises(RequiredIsMissing):
            loader1.load(max_records=2, force_requirements=False)


def test_load_requiredisrunning(loader1):
    with mock.patch("etools_datamart.apps.mart.data.models.Intervention.loader.check_refresh", lambda *a: True):
        with mock.patch("etools_datamart.apps.mart.data.models.Intervention.loader.is_running", lambda *a: True):
            with pytest.raises(RequiredIsRunning):
                loader1.load(max_records=2)


def test_load_requiredready(loader1):
    with mock.patch("etools_datamart.apps.mart.data.models.Intervention.loader.check_refresh", lambda *a: False):
        loader1.load(max_records=2)


def test_load_always_update(loader1):
    with mock.patch("etools_datamart.apps.mart.data.models.Intervention.loader.check_refresh", lambda *a: False):
        loader1.load(max_records=2, always_update=True, only_delta=False)
        ret = loader1.load(max_records=2, always_update=True, only_delta=False)
    assert ret.created == 0
    assert ret.updated == 2


@pytest.mark.django_db
def test_load_no_changes():
    loader1 = Partner.loader
    loader1.model.objects.truncate()
    loader1.load(max_records=2, only_delta=False)
    ret = loader1.load(max_records=2, only_delta=False)
    assert ret.unchanged == 2


def test_load_exception(loader1):
    with mock.patch("%s.process_country" % fqn(loader1), side_effect=Exception()):
        with pytest.raises(Exception):
            loader1.load(
                max_records=2,
            )


def test_load_ignore_dependencies(loader1):
    ret = loader1.load(ignore_dependencies=True, max_records=2)
    assert ret.created == 2


def test_load_lock_fail(loader1):
    loader1.lock()
    ret = loader1.load(ignore_dependencies=True, max_records=2)
    assert ret.created == 0


def test_load_verbosity(loader1):
    ret = loader1.load(ignore_dependencies=True, max_records=2, stdout=StringIO(), verbosity=2)
    assert ret.created == 2


def test_load_error(loader1):
    with mock.patch("%s.results" % fqn(loader1), EtlResult(error="error"), create=True):
        loader1.on_end()


def test_loader_locking(loader1):
    assert not loader1.is_locked
    assert loader1.lock()
    assert loader1.is_locked
    loader1.unlock()
    assert not loader1.is_locked
