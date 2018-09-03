from unittest import mock

import pytest

from etools_datamart.apps.etl.models import TaskLog
from etools_datamart.apps.etl.tasks import load_pmp_indicator


@pytest.fixture(autouse=True)
def setup_module(db):
    TaskLog.objects.filter().delete()
    assert not TaskLog.objects.exists()


def test_load_pmp_indicator(db):
    assert load_pmp_indicator.apply()
    assert TaskLog.objects.filter(task='etl_etools_datamart.apps.etl.load_pmp_indicator',
                                  result='SUCCESS').exists()


@mock.patch('etools_datamart.apps.etl.tasks.load_pmp_indicator.run', side_effect=Exception)
def test_load_pmp_indicator_fail(db):
    assert load_pmp_indicator.apply()
    assert TaskLog.objects.filter(task='etl_etools_datamart.apps.etl.load_pmp_indicator',
                                  result='FAILURE')
