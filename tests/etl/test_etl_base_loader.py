# -*- coding: utf-8 -*-
import time
from io import StringIO
from unittest import mock

import pytest

from etools_datamart.apps.data.loader import EtlResult, RequiredIsMissing, RequiredIsRunning
from etools_datamart.apps.data.models import FundsReservation


@pytest.fixture()
def loader1(db):
    loader = FundsReservation.loader
    loader.config.lock_key = str(time.time())
    return loader


def test_load_requiredismissing(loader1):
    with mock.patch('etools_datamart.apps.data.models.Intervention.loader.need_refresh', lambda *a: True):
        with pytest.raises(RequiredIsMissing):
            loader1.load(check_requirements=True, max_records=2)


def test_load_requiredisrunning(loader1):
    with mock.patch('etools_datamart.apps.data.models.Intervention.loader.need_refresh', lambda *a: True):
        with mock.patch('etools_datamart.apps.data.models.Intervention.loader.is_running', lambda *a: True):
            with pytest.raises(RequiredIsRunning):
                loader1.load(check_requirements=False, max_records=2)


def test_load_requiredsuccess(loader1):
    with mock.patch('etools_datamart.apps.data.models.Intervention.loader.need_refresh', lambda *a: True):
        with mock.patch('etools_datamart.apps.data.models.Intervention.loader.load', lambda *a, **kw: True):
            loader1.load(check_requirements=False, max_records=2)


def test_load_requiredready(loader1):
    with mock.patch('etools_datamart.apps.data.models.Intervention.loader.need_refresh', lambda *a: False):
        loader1.load(check_requirements=False, max_records=2)


def test_load_always_update(loader1):
    with mock.patch('etools_datamart.apps.data.models.Intervention.loader.need_refresh', lambda *a: False):
        loader1.load(check_requirements=False, max_records=2, always_update=True)
        ret = loader1.load(check_requirements=False, max_records=2, always_update=True)
    assert ret.created == 0
    assert ret.updated == 2


def test_load_no_changes(loader1):
    with mock.patch('etools_datamart.apps.data.models.Intervention.loader.need_refresh', lambda *a: False):
        loader1.load(check_requirements=False, max_records=2)
        ret = loader1.load(check_requirements=False, max_records=2)
    assert ret.unchanged == 2


def test_load_exception(loader1):
    with mock.patch('etools_datamart.apps.data.models.FundsReservation.loader.process_country',
                    side_effect=Exception()):
        with pytest.raises(Exception):
            loader1.load(check_requirements=False, max_records=2)


def test_load_ignore_dependencies(loader1):
    ret = loader1.load(ignore_dependencies=True, max_records=2)
    assert ret.created == 2


def test_load_lock_fail(loader1):
    loader1.lock()
    ret = loader1.load(ignore_dependencies=True, max_records=2)
    assert ret.created == 0


def test_load_verbosity(loader1):
    ret = loader1.load(ignore_dependencies=True, max_records=2,
                       stdout=StringIO(), verbosity=2)
    assert ret.created == 2


def test_load_error(loader1):
    with mock.patch('etools_datamart.apps.data.models.FundsReservation.loader.results',
                    EtlResult(error="error")):
        loader1.on_end()


def test_loader_locking(loader1):
    assert not loader1.is_locked
    assert loader1.lock()
    assert loader1.is_locked
    loader1.unlock()
    assert not loader1.is_locked

#
# def test_load_pmp_indicator(number_of_intervention):
#     PMPIndicators.objects.truncate()
#     PMPIndicators.loader.unlock()
#     assert PMPIndicators.loader.load() == EtlResult(created=153)
#     assert PMPIndicators.objects.count() == number_of_intervention * 3
#
#
# def test_load_intervention(number_of_intervention, settings, monkeypatch):
#     Intervention.loader.unlock()
#     assert Intervention.loader.load() == EtlResult(created=number_of_intervention * 3)
#     assert Intervention.objects.count() == number_of_intervention * 3
#
#
# def test_load_fam_indicator(db, settings, monkeypatch):
#     FAMIndicator.loader.unlock()
#     FAMIndicator.loader.load()
#     assert FAMIndicator.objects.count() == 3
#
#
# def test_load_user_stats(db, settings, monkeypatch):
#     UserStats.loader.unlock()
#     UserStats.loader.load()
#     assert UserStats.objects.count() == 3
#
#
# def test_load_location(db, settings, monkeypatch):
#     Location.loader.unlock()
#     Location.loader.load()
#     assert UserStats.objects.count() == 3
#
#
# def test_load_hact(db, settings, monkeypatch):
#     HACT.loader.unlock()
#     HACT.loader.load()
#     assert HACT.objects.count() == 3
#     bolivia = HACT.objects.get(country_name='Bolivia')
#     assert bolivia.microassessments_total == 0
#     assert bolivia.programmaticvisits_total == 1
#     assert bolivia.followup_spotcheck == 0
#     assert bolivia.completed_spotcheck == 0
#     assert bolivia.completed_hact_audits == 0
#     assert bolivia.completed_special_audits == 0
#     res = HACT.loader.load()
#     assert res == EtlResult(unchanged=3)
#
#
# @freeze_time("2018-11-10")
# def test_dataset_increased(db, settings, monkeypatch):
#     UserStats.loader.unlock()
#     UserStats.loader.load()
#     UserStats.objects.first().delete()
#     ret = UserStats.loader.load()
#     assert ret == EtlResult(created=1, unchanged=2)
#
#
# @freeze_time("2018-11-10")
# def test_dataset_changed(db, settings, monkeypatch):
#     UserStats.loader.unlock()
#     ret = UserStats.loader.load()
#     assert ret == EtlResult(created=3)
#     UserStats.objects.update(total=999, unicef=999)
#
#     ret = UserStats.loader.load()
#     assert ret == EtlResult(updated=3)
