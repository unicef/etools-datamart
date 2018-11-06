# -*- coding: utf-8 -*-
from celery.signals import task_postrun
from django.apps import AppConfig

from etools_datamart.apps.etl.signals import data_refreshed


class Config(AppConfig):
    name = 'etools_datamart.apps.etl'

    def ready(self):
        pass
        # from etools_datamart.apps.data.signals import table_truncated
        # from etools_datamart.apps.data.models.base import DataMartModel
        # table_truncated.connect(invalidate_cache)


@task_postrun.connect
def task_postrun_handler(signal, sender, task_id, task, args, kwargs, retval, state, **kw):
    if not hasattr(sender, 'linked_model'):
        return
    data_refreshed.send(sender.linked_model)
