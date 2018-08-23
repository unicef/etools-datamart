# -*- coding: utf-8 -*-
import logging

from etools_datamart.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def ping():
    print("Ping")
