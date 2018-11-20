import os
from time import time

from celery import Celery
from celery.signals import task_postrun, task_prerun
from celery.task import Task
from django.utils import timezone

from etools_datamart.apps.etl.lock import only_one

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etools_datamart.config.settings')


class ETLTask(Task):
    abstract = True
    linked_model = None


class DatamartCelery(Celery):
    etl_cls = ETLTask
    _mapping = {}

    def _task_from_fun(self, fun, name=None, base=None, bind=False, **options):
        linked_model = options.get('linked_model', None)
        name = name or self.gen_task_name(fun.__name__, fun.__module__)
        options['lock_key'] = f"{name}-lock"
        fun = only_one(fun, options['lock_key'])
        options['unlock'] = fun.unlock

        task = super()._task_from_fun(fun, name=name, base=None, bind=False, **options)
        if linked_model:
            linked_model._etl_task = task
            linked_model._etl_loader = fun

        return task

    def etl(self, model, *args, **opts):
        opts['base'] = ETLTask
        opts['linked_model'] = model
        task = super().task(*args, **opts)
        return task

    def get_all_etls(self):
        return [cls for (name, cls) in self.tasks.items() if hasattr(cls, 'linked_model')]

    # def gen_task_name(self, name, module):
    #     prefix = ""
    #     if module.endswith('.tasks.etl'):
    #         module = module[:-10]
    #         prefix = 'etl_'
    #     if module.endswith('.tasks'):
    #         module = module[:-6]
    #     return prefix + super(DatamartCelery, self).gen_task_name(name, module)


app = DatamartCelery('datamart')
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()],
#                        related_name='tasks')
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()],
#                        related_name='etl')

app.timers = {}


@task_prerun.connect
def task_prerun_handler(signal, sender, task_id, task, args, kwargs, **kw):
    if not hasattr(sender, 'linked_model'):
        return

    app.timers[task_id] = time()
    from django.contrib.contenttypes.models import ContentType
    from etools_datamart.apps.etl.models import EtlTask

    defs = {'result': 'RUNNING',
            'timestamp': timezone.now()}
    EtlTask.objects.update_or_create(task=task.name,
                                     content_type=ContentType.objects.get_for_model(task.linked_model),
                                     table_name=task.linked_model._meta.db_table,
                                     defaults=defs)


@task_postrun.connect
def task_postrun_handler(signal, sender, task_id, task, args, kwargs, retval, state, **kw):
    if not hasattr(sender, 'linked_model'):
        return
    try:
        cost = time() - app.timers.pop(task_id)
    except KeyError:  # pragma: no cover
        cost = -1
    defs = {'elapsed': cost,
            'result': state,
            'timestamp': timezone.now()}
    if state == 'SUCCESS':
        defs['last_success'] = timezone.now()
    else:
        defs['last_failure'] = timezone.now()
    from etools_datamart.apps.etl.models import EtlTask

    EtlTask.objects.update_or_create(task=task.name, defaults=defs)
    app.timers[task.name] = cost
