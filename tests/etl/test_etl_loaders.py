# -*- coding: utf-8 -*-
from etools_datamart.apps.etl.tasks import (FAMIndicator, HACT, Intervention, load_fam_indicator,
                                            load_hact, load_intervention, load_pmp_indicator,
                                            load_user_report, PMPIndicators, UserStats,)


def test_load_pmp_indicator(number_of_intervention):
    load_pmp_indicator.unlock()
    assert load_pmp_indicator() == {'Bolivia': number_of_intervention,
                                    'Chad': number_of_intervention,
                                    'Lebanon': number_of_intervention}
    assert PMPIndicators.objects.count() == number_of_intervention * 3


def test_load_intervention(number_of_intervention, settings, monkeypatch):
    load_intervention.unlock()
    load_intervention()
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
