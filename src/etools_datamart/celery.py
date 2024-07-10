# import json
import os

import sentry_sdk
from celery import Celery
from celery.signals import task_failure
from celery.utils.log import get_logger
from kombu import Exchange, Queue
from kombu.serialization import register

from etools_datamart.apps.etl.results import etl_dumps, etl_loads

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "etools_datamart.config.settings")

logger = get_logger(__name__)


def handle_task_failure(sender, task, task_id, exception=None, args=None, kwargs=None, traceback=None, **kw):

    logger.error(f"Task {task.name} (ID: {task_id}) failed: {exception}")

    with sentry_sdk.push_scope() as scope:
        scope.set_extra("task_id", task_id)
        scope.set_extra("task_name", task.name)
        scope.set_extra("traceback", traceback)
        scope.set_extra("args", args)
        scope.set_extra("kwargs", kwargs)

        for key, value in kw:
            scope.set_extra(key, value)

        if exception:
            sentry_sdk.capture_exception(exception)


class DatamartCelery(Celery):
    _mapping = {}

    def get_all_etls(self):
        return [cls for (name, cls) in self.tasks.items() if hasattr(cls, "linked_model")]


app = DatamartCelery("datamart")

task_failure.connect(handle_task_failure)

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])  # pragma

app.timers = {}
app.conf.task_queues = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("etl", Exchange("etl"), routing_key="etl.#"),
    Queue("mail", Exchange("mail"), routing_key="mail.#"),
    Queue("subscription", Exchange("subscription"), routing_key="subscription.#"),
)
app.conf.task_default_queue = "default"
app.conf.task_default_exchange_type = "direct"
app.conf.task_default_routing_key = "default"
app.conf.task_routes = {"send_queued_mail": {"queue": "mail"}}
app.conf.task_routes = {"djcelery_email_send_multiple": {"queue": "mail"}}
app.conf.task_routes = {"etools_datamart.apps.etl.subscriptions.tasks.*": {"queue": "subscription"}}

register("etljson", etl_dumps, etl_loads, content_type="application/x-myjson", content_encoding="utf-8")
