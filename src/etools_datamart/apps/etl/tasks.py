import logging

from django.core.cache import cache
from django.utils import timezone

from etools_datamart.celery import app

logger = logging.getLogger(__name__)

HEALTHCHECK_KEY = 'healthcheck'
HEALTHCHECK_FORMAT = '%Y-%m-%d %H:%M:%S'


@app.task
def healthcheck():
    cache.set('healthcheck', timezone.now().strftime(HEALTHCHECK_FORMAT))

#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(60.0, healthcheck.s(), name='healthcheck')
