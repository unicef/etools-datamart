import os
from time import time

from celery import Celery
from celery.app.task import TaskType
from celery.signals import task_postrun, task_prerun
from celery.task import Task
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from etools_datamart.apps.etl.lock import only_one

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etools_datamart.config.settings')


class ETLTask(Task, metaclass=TaskType):
    abstract = True


class DatamartCelery(Celery):
    etl_cls = ETLTask
    _mapping = {}

    def _task_from_fun(self, fun, name=None, base=None, bind=False, **options):
        model = None
        if 'model' in options:
            model = options.pop('model')
            model._etl_loader = fun
        fun = only_one(fun, f"{name}-lock")
        task = super()._task_from_fun(fun, name=None, base=None, bind=False, **options)
        if model:
            task._model = model
            model._etl_task = task
        return task

    def etl(self, model, *args, **opts):
        opts['base'] = ETLTask
        opts['model'] = model
        task = super().task(*args, **opts)
        return task

    def gen_task_name(self, name, module):
        prefix = ""
        if module.endswith('.tasks.etl'):
            module = module[:-10]
            prefix = 'etl_'
        if module.endswith('.tasks'):
            module = module[:-6]
        return prefix + super(DatamartCelery, self).gen_task_name(name, module)


app = DatamartCelery('datamart')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(related_name='tasks')
app.autodiscover_tasks(related_name='etl')

app.timers = {}


@task_prerun.connect
def task_prerun_handler(signal, sender, task_id, task, args, kwargs, **kw):
    app.timers[task_id] = time()


@task_postrun.connect
def task_postrun_handler(signal, sender, task_id, task, args, kwargs, retval, state, **kw):
    try:
        cost = time() - app.timers.pop(task_id)
    except KeyError:  # pragma: no cover
        cost = -1
    from etools_datamart.apps.etl.models import TaskLog
    defs = {'elapsed': cost,
            'result': state,
            'timestamp': timezone.now()}
    if state == 'SUCCESS':
        defs['last_success'] = timezone.now()
    else:
        defs['last_failure'] = timezone.now()

    TaskLog.objects.update_or_create(task=task.name,
                                     content_type=ContentType.objects.get_for_model(task._model),
                                     table_name=task._model._meta.db_table,
                                     defaults=defs)
    app.timers[task.name] = cost
