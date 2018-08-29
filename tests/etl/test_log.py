# -*- coding: utf-8 -*-

from etools_datamart.apps.etl.models import Execution
from etools_datamart.apps.etl.tasks import load_intervention, Intervention


def test_log(db):
    load_intervention.apply()
    log = Execution.objects.get(task=Intervention._etl_task.name)
    assert log.table_name == Intervention._meta.db_table
    assert log.content_type.model_class() == Intervention
    assert log.result == 'SUCCESS'
