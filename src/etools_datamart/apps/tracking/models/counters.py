# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.db import models
from unicef_rest_framework.models import Service

logger = logging.getLogger(__name__)


class DailyCounter(models.Model):
    day = models.DateField(db_index=True)
    total = models.IntegerField(db_index=True)
    cached = models.IntegerField(db_index=True)
    user = models.IntegerField(db_index=True)
    response_max = models.IntegerField(db_index=True)
    response_min = models.IntegerField(db_index=True)
    response_average = models.FloatField(db_index=True)
    unique_ips = models.IntegerField(db_index=True)

    class Meta:
        unique_together = ('day',)
        ordering = ('-day',)

    def __unicode__(self):
        return self.day.strftime('%d %b %Y')


class MonthlyCounter(models.Model):
    day = models.DateField(db_index=True)
    total = models.IntegerField(db_index=True)
    cached = models.IntegerField(db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    response_max = models.IntegerField(db_index=True)
    response_min = models.IntegerField(db_index=True)
    response_average = models.FloatField(db_index=True)
    unique_ips = models.IntegerField(db_index=True)

    class Meta:
        unique_together = ('day',)
        ordering = ('-day',)

    def __unicode__(self):
        return self.day.strftime('%b %Y')


class PathCounter(models.Model):
    day = models.DateField(db_index=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                blank=True, null=True)
    path = models.CharField(max_length=255, db_index=True)
    total = models.IntegerField(db_index=True)
    cached = models.IntegerField(db_index=True)
    response_max = models.IntegerField(db_index=True)
    response_min = models.IntegerField(db_index=True)

    class Meta:
        unique_together = ('day', 'path')
        ordering = ('-day',)

    def __unicode__(self):
        return self.path


class UserCounter(models.Model):
    day = models.DateField(db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    total = models.IntegerField(db_index=True)
    cached = models.IntegerField(db_index=True)
    response_max = models.IntegerField(db_index=True)
    response_min = models.IntegerField(db_index=True)

    class Meta:
        unique_together = ('day', 'user')
        ordering = ('-day',)

    def __unicode__(self):
        return self.day.strftime('%Y %m %d')
