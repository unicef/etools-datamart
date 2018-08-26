import os

from celery import Celery
# set the default Django settings module for the 'celery' program.
from celery.app.task import TaskType
from celery.task import Task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etools_datamart.config.settings')


class ETLTask(Task, metaclass=TaskType):
    abstract = True


class DatamartCelery(Celery):
    etl_cls = ETLTask
    _mapping = {}

    def task(self, *args, **opts):
        return super().task(*args, **opts)

    def _task_from_fun(self, fun, name=None, base=None, bind=False, **options):
        if 'model' in options:
            model = options.pop('model')
            model._etl_loader = fun
        return super()._task_from_fun(fun, name=None, base=None, bind=False, **options)

    def etl(self, model, *args, **opts):
        opts['base'] = ETLTask
        opts['model'] = model
        task = super().task(*args, **opts)
        return task

    def gen_task_name(self, name, module):
        prefix = ""
        if module.endswith('.tasks.etl'):
            module = module[:-10]
            # prefix = 'etl_'
        if module.endswith('.tasks'):
            module = module[:-6]
        return prefix + super(DatamartCelery, self).gen_task_name(name, module)


app = DatamartCelery('datamart')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(related_name='tasks')
app.autodiscover_tasks(related_name='etl')
