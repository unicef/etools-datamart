from unittest import mock

import pytest
from celery.signals import task_postrun

from unicef_security.models import User

from etools_datamart.apps.data.loader import EtlResult
from etools_datamart.apps.data.models import HACT, PMPIndicators
from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.celery import task_postrun_handler

pytestmarker = pytest.mark.django_db


def test_load_pmp_indicator(db):
    with mock.patch('etools_datamart.apps.data.models.PMPIndicators.loader.task.run',
                    return_value=EtlResult(created=11)):
        assert PMPIndicators.loader.task.apply()
        assert EtlTask.objects.filter(task=PMPIndicators.loader.task.name,
                                      results__created=11,
                                      status='SUCCESS').exists()


def test_load_pmp_indicator_fail(db):
    with mock.patch('etools_datamart.apps.data.models.PMPIndicators.loader.task.run', side_effect=Exception):
        assert PMPIndicators.loader.task.apply()
        assert EtlTask.objects.filter(task=PMPIndicators.loader.task.name,
                                      status='FAILURE')


@pytest.fixture()
def disable_post_run():
    task_postrun.disconnect(task_postrun_handler)
    yield
    task_postrun.connect(task_postrun_handler)


def test_load_pmp_indicator_running(db, disable_post_run):
    with mock.patch('etools_datamart.apps.data.models.PMPIndicators.loader.task.run'):
        assert PMPIndicators.loader.task.apply()
        assert EtlTask.objects.filter(task=PMPIndicators.loader.task.name,
                                      status='RUNNING')


def test_no_changes(db):
    with mock.patch('etools_datamart.apps.data.models.PMPIndicators.loader.task.run',
                    return_value=EtlResult()):
        assert PMPIndicators.loader.task.apply()
        assert EtlTask.objects.filter(task=PMPIndicators.loader.task.name,
                                      status='SUCCESS').exists()


def test_manager(db):
    # TaskLogFactory(content_type=ContentType.objects.get_for_model(HACT))
    assert EtlTask.objects.filter_for_models(HACT)
    assert EtlTask.objects.get_for_model(HACT)
    with pytest.raises(EtlTask.DoesNotExist):
        assert EtlTask.objects.get_for_model(User)
