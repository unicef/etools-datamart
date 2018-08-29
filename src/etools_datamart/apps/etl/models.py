# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db import models


class TaskLog(models.Model):
    task = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True)
    result = models.CharField(max_length=200)
    elapsed = models.IntegerField()
    last_success = models.DateTimeField(null=True)
    last_failure = models.DateTimeField(null=True)
    table_name = models.CharField(max_length=200, null=True)
    content_type = models.ForeignKey(ContentType, models.CASCADE, null=True)

    def __str__(self):
        return self.task
