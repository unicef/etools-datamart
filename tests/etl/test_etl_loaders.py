# -*- coding: utf-8 -*-
from freezegun import freeze_time

from etools_datamart.apps.data.models import FAMIndicator, HACT, Intervention, PMPIndicators, UserStats
from etools_datamart.apps.etl.tasks.etl import (EtlResult, load_fam_indicator, load_hact,
                                                load_intervention, load_pmp_indicator, load_user_report,)


def test_load_pmp_indicator(number_of_intervention):
    load_pmp_indicator.unlock()
    assert load_pmp_indicator() == EtlResult(created=153)
    assert PMPIndicators.objects.count() == number_of_intervention * 3


def test_load_intervention(number_of_intervention, settings, monkeypatch):
    load_intervention.unlock()
    assert load_intervention() == EtlResult(created=number_of_intervention*3)
    assert Intervention.objects.count() == number_of_intervention * 3


def test_load_fam_indicator(db, settings, monkeypatch):
    load_fam_indicator.unlock()
    load_fam_indicator()
    assert FAMIndicator.objects.count() == 3


def test_load_user_stats(db, settings, monkeypatch):
    load_user_report.unlock()
    load_user_report()
    assert UserStats.objects.count() == 3


def test_load_hact(db, settings, monkeypatch):
    load_hact.unlock()
    load_hact()
    assert HACT.objects.count() == 3
    bolivia = HACT.objects.get(country_name='Bolivia')
    assert bolivia.microassessments_total == 0
    assert bolivia.programmaticvisits_total == 1
    assert bolivia.followup_spotcheck == 0
    assert bolivia.completed_spotcheck == 0
    assert bolivia.completed_hact_audits == 0
    assert bolivia.completed_special_audits == 0
    res = load_hact()
    assert res == EtlResult(unchanged=3)


@freeze_time("2018-11-10")
def test_dataset_increased(db, settings, monkeypatch):
    load_user_report.unlock()
    load_user_report()
    UserStats.objects.first().delete()
    ret = load_user_report()
    assert ret == EtlResult(created=1, unchanged=2)


@freeze_time("2018-11-10")
def test_dataset_changed(db, settings, monkeypatch):
    load_user_report.unlock()
    ret = load_user_report()
    assert ret == EtlResult(created=3)
    UserStats.objects.update(total=999, unicef=999)

    ret = load_user_report()
    assert ret == EtlResult(updated=3)
