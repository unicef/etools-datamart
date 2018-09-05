# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.conf import settings
from django.db import models
from django.db.models import SET_NULL
from strategy_field.fields import StrategyClassField
# from .models import Service
# from .utils import get_hostname
from unicef_rest_framework.models import Service

logger = logging.getLogger(__name__)


class APIRequestLogManager(models.Manager):
    def aggregate(self):
        from .aggregate import aggregate_log

        return aggregate_log()


class APIRequestLog(models.Model):
    """Logs API requests by time, user, etc"""
    # user or None for anon
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                             null=True, blank=True)

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
    query_params = models.TextField(db_index=True)

    # POST body data
    data = models.TextField(null=True, blank=True)
    content_type = models.CharField(max_length=255)
    cached = models.BooleanField(default=False)

    # extra
    service = models.ForeignKey(Service,
                                blank=True, null=True, on_delete=SET_NULL)
    viewset = StrategyClassField(blank=True, null=True)

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    objects = APIRequestLogManager()

    def __unicode__(self):
        return "{0.requested_at} {0.path}".format(self)
