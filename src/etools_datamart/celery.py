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
