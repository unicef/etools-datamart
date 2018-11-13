from unittest import mock

import pytest
from celery.signals import task_postrun

from etools_datamart.apps.data.models import PMPIndicators
from etools_datamart.apps.etl.models import TaskLog
from etools_datamart.apps.etl.tasks import load_pmp_indicator
from etools_datamart.celery import task_postrun_handler

pytestmarker = pytest.mark.django_db


def test_check_extra_attributes(db):
    assert (TaskLog.objects.get_for_task(load_pmp_indicator) ==
            TaskLog.objects.get_for_model(PMPIndicators))


#     assert load_pmp_indicator.linked_model
#     assert load_pmp_indicator.linked_model.task_log
#     assert PMPIndicators.task_log.table_name == PMPIndicators._meta.db_table


def test_load_pmp_indicator(db):
    with mock.patch('etools_datamart.apps.etl.tasks.load_pmp_indicator.run'):
        assert load_pmp_indicator.apply()
        assert TaskLog.objects.filter(task='etl_etools_datamart.apps.etl.load_pmp_indicator',
                                      result='SUCCESS').exists()


def test_load_pmp_indicator_fail(db):
    with mock.patch('etools_datamart.apps.etl.tasks.load_pmp_indicator.run', side_effect=Exception):
        assert load_pmp_indicator.apply()
        assert TaskLog.objects.filter(task='etl_etools_datamart.apps.etl.load_pmp_indicator',
                                      result='FAILURE')


@pytest.fixture()
def disable_post_run():
    task_postrun.disconnect(task_postrun_handler)
    yield
    task_postrun.connect(task_postrun_handler)


def test_load_pmp_indicator_running(db, disable_post_run):
    with mock.patch('etools_datamart.apps.etl.tasks.load_pmp_indicator.run'):
        assert load_pmp_indicator.apply()
        assert TaskLog.objects.filter(task='etl_etools_datamart.apps.etl.load_pmp_indicator',
                                      result='RUNNING')
