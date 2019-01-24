# import json
import os

from celery import Celery
from kombu import Exchange, Queue
from kombu.serialization import register

from etools_datamart.apps.etl.results import etl_dumps, etl_loads

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etools_datamart.config.settings')


class DatamartCelery(Celery):
    _mapping = {}

    def get_all_etls(self):
        return [cls for (name, cls) in self.tasks.items() if hasattr(cls, 'linked_model')]


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
app.conf.task_routes = {'send_queued_mail': {'queue': 'mail'}}
app.conf.task_routes = {'etools_datamart.apps.etl.subscriptions.tasks.*': {'queue': 'subscription'}}

register('etljson', etl_dumps, etl_loads,
         content_type='application/x-myjson', content_encoding='utf-8')


# @task_prerun.connect
# def task_prerun_handler(signal, sender, task_id, task, args, kwargs, **kw):
#     if not hasattr(sender, 'linked_model'):
#         return
#
#     app.timers[task_id] = time()
#     from django.contrib.contenttypes.models import ContentType
#     from etools_datamart.apps.etl.models import EtlTask
#     from django.utils import timezone
#     defs = {'status': 'RUNNING',
#             'last_run': timezone.now()}
#     EtlTask.objects.update_or_create(task=task.name,
#                                      content_type=ContentType.objects.get_for_model(task.linked_model),
#                                      table_name=task.linked_model._meta.db_table,
#                                      defaults=defs)
#
#
#
# @task_postrun.connect
# def task_postrun_handler(signal, sender, task_id, task, args, kwargs, retval, state, **kw):
#     from django.utils import timezone
#     from etools_datamart.apps.subscriptions.models import Subscription
#     from etools_datamart.apps.etl.models import EtlTask
#     logger = get_task_logger('etl')
#     if not hasattr(sender, 'linked_model'):
#         return
#     try:
#         cost = time() - app.timers.pop(task_id)
#     except KeyError:  # pragma: no cover
#         cost = -1
#     defs = {'elapsed': cost,
#             'status': state}
#
#     if state == 'SUCCESS':
#         try:
#             defs['results'] = retval.as_dict()
#             if not retval.error:
#                 if retval.created > 0 or retval.updated > 0:
#                     defs['last_changes'] = timezone.now()
#                     for service in sender.linked_model.linked_services:
#                         service.invalidate_cache()
#                         Subscription.objects.notify(sender.linked_model)
#                 defs['last_success'] = timezone.now()
#             else:
#                 defs['status'] = 'ERROR'
#         except Exception as e:  # pragma: no cover
#             logger.error(e)
#             defs['results'] = str(retval)
#     else:
#         # if not isinstance(retval, dict):
#         defs['results'] = str(retval)
#         defs['last_failure'] = timezone.now()
#
#     EtlTask.objects.update_or_create(task=task.name, defaults=defs)
#     app.timers[task.name] = cost
