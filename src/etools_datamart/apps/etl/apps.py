from django.apps import AppConfig

from celery.signals import task_postrun

from etools_datamart.apps.etl.signals import data_refreshed


class Config(AppConfig):
    name = 'etools_datamart.apps.etl'


@task_postrun.connect
def task_postrun_handler(signal, sender, task_id, task, args, kwargs, retval, state, **kw):
    if not hasattr(sender, 'linked_model'):
        return
    data_refreshed.send(sender.linked_model)
