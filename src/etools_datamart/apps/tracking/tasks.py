# -*- coding: utf-8 -*-
from celery.utils.log import get_task_logger

from etools_datamart.celery import app

from .models import APIRequestLog

task_logger = get_task_logger(__name__)


@app.task
def task_aggregate_log():
    task_logger.info('Starting logs aggregation')
    return APIRequestLog.objects.aggregate()
