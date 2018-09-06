# -*- coding: utf-8 -*-

import logging

from django.db import connection, models
from strategy_field.fields import StrategyClassField

logger = logging.getLogger(__name__)


class APIRequestLogManager(models.Manager):
    def aggregate(self):
        from .aggregate import aggregate_log

        return aggregate_log()

    def truncate(self):
        cursor = connection.cursor()
        cursor.execute(f'TRUNCATE TABLE "{self.model._meta.db_table}"')


class APIRequestLog(models.Model):
    """Logs API requests by time, user, etc"""
    # user or None for anon
    user = models.CharField(max_length=100, null=True, blank=True, db_index=True)

    # timestamp of request
    requested_at = models.DateTimeField(db_index=True)

    # number of milliseconds to respond
    response_ms = models.PositiveIntegerField('ms', default=0)
    response_length = models.PositiveIntegerField('length', default=0)

    # request path
    path = models.CharField(max_length=255, db_index=True)

    # remote IP address of request
    remote_addr = models.GenericIPAddressField()

    # originating host of request
    host = models.URLField()

    # HTTP method (GET, etc)
    method = models.CharField(max_length=10)

    # query params
    query_params = models.TextField()

    # POST body data
    data = models.TextField(null=True, blank=True)
    content_type = models.CharField(max_length=255)
    cached = models.BooleanField(default=False)

    # extra
    service = models.CharField(max_length=100, blank=True, null=True)
    viewset = StrategyClassField(blank=True, null=True)

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        ordering = ('-id', )

    objects = APIRequestLogManager()

    def __str__(self):
        return f"{self.requested_at} {self.path}"
