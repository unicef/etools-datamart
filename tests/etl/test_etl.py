# -*- coding: utf-8 -*-
from etools_datamart.apps.etl.tasks import Intervention, load_intervention, load_pmp_indicator, PMPIndicators


def test_load_pmp_indicator(db):
    assert load_pmp_indicator() == {'Bolivia': 7, 'Chad': 7, 'Lebanon': 7}
    assert PMPIndicators.objects.count() == 21


def test_load_intervention(db):
    load_intervention()
    assert Intervention.objects.count() == 21
