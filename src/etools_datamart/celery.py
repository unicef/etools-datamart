# import json
import os
from time import time

from celery import Celery
# from celery.contrib.abortable import AbortableTask
from celery.signals import task_postrun, task_prerun
from kombu import Exchange, Queue
from kombu.serialization import register

from etools_datamart.apps.etl.results import etl_dumps, etl_loads

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etools_datamart.config.settings')


# class ETLTask(AbortableTask):
#     abstract = True
#     linked_model = None


class DatamartCelery(Celery):
    # etl_cls = ETLTask
    _mapping = {}

    # def _task_from_fun(self, fun, name=None, base=None, bind=False, **options):
    #     from etools_datamart.apps.etl.lock import only_one
    #     linked_model = options.get('linked_model', None)
    #     if linked_model:
    #         name = name or self.gen_task_name(fun.__name__, fun.__module__)
    #         options['lock_key'] = f"{name}-lock"
    #         fun = only_one(fun, options['lock_key'])
    #         # options['unlock'] = fun.unlock
    #         task = super()._task_from_fun(fun, name=name, base=None, bind=False, **options)
    #         linked_model._etl_task = task
    #         linked_model._etl_loader = fun
    #     else:
    #         task = super()._task_from_fun(fun, name=name, base=None, bind=False, **options)
    #     return task
    #
    # def etl(self, model, *args, **opts):
    #     opts['base'] = ETLTask
    #     opts['linked_model'] = model
    #     task = super().task(*args, **opts)
    #     return task

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
app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])  # pragma

app.timers = {}
app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('etl', Exchange('etl'), routing_key='etl.#'),
    Queue('mail', Exchange('mail'), routing_key='mail.#'),
    Queue('subscription', Exchange('subscription'), routing_key='subscription.#'),
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'
app.conf.task_routes = {'etools_datamart.apps.etl.tasks.etl.*': {'queue': 'etl'}}
app.conf.task_routes = {'send_queued_mail': {'queue': 'mail'}}
app.conf.task_routes = {'etools_datamart.apps.etl.subscriptions.tasks.*': {'queue': 'subscription'}}


@task_prerun.connect
def task_prerun_handler(signal, sender, task_id, task, args, kwargs, **kw):
    if not hasattr(sender, 'linked_model'):
        return

    app.timers[task_id] = time()
    from django.contrib.contenttypes.models import ContentType
    from etools_datamart.apps.etl.models import EtlTask
    from django.utils import timezone
    defs = {'status': 'RUNNING',
            'last_run': timezone.now()}
    EtlTask.objects.update_or_create(task=task.name,
                                     content_type=ContentType.objects.get_for_model(task.linked_model),
                                     table_name=task.linked_model._meta.db_table,
                                     defaults=defs)


register('etljson', etl_dumps, etl_loads,
         content_type='application/x-myjson', content_encoding='utf-8')


@task_postrun.connect
def task_postrun_handler(signal, sender, task_id, task, args, kwargs, retval, state, **kw):
    from django.utils import timezone
    from etools_datamart.apps.subscriptions.models import Subscription
    from etools_datamart.apps.etl.models import EtlTask
    if not hasattr(sender, 'linked_model'):
        return
    try:
        cost = time() - app.timers.pop(task_id)
    except KeyError:  # pragma: no cover
        cost = -1
    defs = {'elapsed': cost,
            'status': state}

    if state == 'SUCCESS':
        try:
            defs['results'] = retval.as_dict()
        except Exception:  # pragma: no cover
            defs['results'] = str(retval)
        if retval.created > 0 or retval.updated > 0:
            defs['last_changes'] = timezone.now()
            for service in sender.linked_model.linked_services:
                service.invalidate_cache()
                Subscription.objects.notify(sender.linked_model)

        defs['last_success'] = timezone.now()
    else:
        # if not isinstance(retval, dict):
        defs['results'] = str(retval)
        defs['last_failure'] = timezone.now()

    EtlTask.objects.update_or_create(task=task.name, defaults=defs)
    app.timers[task.name] = cost
