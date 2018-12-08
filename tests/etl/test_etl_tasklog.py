from unittest import mock

import pytest
from celery.signals import task_postrun
from django.contrib.contenttypes.models import ContentType
from test_utilities.factories import TaskLogFactory
from unicef_security.models import User

from etools_datamart.apps.data.models import HACT, PMPIndicators
from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.apps.etl.results import EtlResult
from etools_datamart.apps.etl.tasks.etl import load_pmp_indicator
from etools_datamart.celery import task_postrun_handler

pytestmarker = pytest.mark.django_db


def test_check_extra_attributes(db):
    assert (EtlTask.objects.get_for_task(load_pmp_indicator) ==
            EtlTask.objects.get_for_model(PMPIndicators))


def test_load_pmp_indicator(db):
    with mock.patch('etools_datamart.apps.etl.tasks.etl.load_pmp_indicator.run',
                    return_value=EtlResult(created=11)):
        assert load_pmp_indicator.apply()
        assert EtlTask.objects.filter(task='etools_datamart.apps.etl.tasks.etl.load_pmp_indicator',
                                      results__created=11,
                                      status='SUCCESS').exists()


def test_load_pmp_indicator_fail(db):
    with mock.patch('etools_datamart.apps.etl.tasks.etl.load_pmp_indicator.run', side_effect=Exception):
        assert load_pmp_indicator.apply()
        assert EtlTask.objects.filter(task='etools_datamart.apps.etl.tasks.etl.load_pmp_indicator',
                                      status='FAILURE')


@pytest.fixture()
def disable_post_run():
    task_postrun.disconnect(task_postrun_handler)
    yield
    task_postrun.connect(task_postrun_handler)


def test_load_pmp_indicator_running(db, disable_post_run):
    with mock.patch('etools_datamart.apps.etl.tasks.etl.load_pmp_indicator.run'):
        assert load_pmp_indicator.apply()
        assert EtlTask.objects.filter(task='etools_datamart.apps.etl.tasks.etl.load_pmp_indicator',
                                      status='RUNNING')


def test_no_changes(db):
    with mock.patch('etools_datamart.apps.etl.tasks.etl.load_pmp_indicator.run',
                    return_value=EtlResult()):
        assert load_pmp_indicator.apply()
        assert EtlTask.objects.filter(task='etools_datamart.apps.etl.tasks.etl.load_pmp_indicator',
                                      status='SUCCESS').exists()


def test_manager(db):
    TaskLogFactory(content_type=ContentType.objects.get_for_model(HACT))
    assert EtlTask.objects.filter_for_models(HACT)
    assert EtlTask.objects.get_for_model(HACT)
    with pytest.raises(EtlTask.DoesNotExist):
        assert EtlTask.objects.get_for_model(User)
