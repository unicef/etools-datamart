# -*- coding: utf-8 -*-
from etools_datamart.apps.etl.tasks import (FAMIndicator, Intervention, load_fam_indicator,
                                            load_intervention, load_pmp_indicator, PMPIndicators,)


def test_load_pmp_indicator(number_of_intervention):
    assert load_pmp_indicator() == {'Bolivia': number_of_intervention,
                                    'Chad': number_of_intervention,
                                    'Lebanon': number_of_intervention}
    assert PMPIndicators.objects.count() == number_of_intervention * 3


def test_load_intervention(number_of_intervention, settings, monkeypatch):
    load_intervention()
    assert Intervention.objects.count() == number_of_intervention * 3


def test_load_fam_indicator(db, settings, monkeypatch):
    load_fam_indicator()
    assert FAMIndicator.objects.count() == 3
