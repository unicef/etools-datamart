# -*- coding: utf-8 -*-
from etools_datamart.apps.tracking import utils


def test_reset_all_counters(db):
    utils.reset_all_counters()


def test_refresh_all_counters(db):
    utils.refresh_all_counters()


def test_get_all_counters(db):
    assert utils.get_all_counters() == utils.get_all_counters()
