# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db import models

from etools_datamart.celery import app


class TaskLogManager(models.Manager):
    def inspect(self):
        tasks = [cls for (name, cls) in app.tasks.items() if name.startswith('etl_')]
        for task in tasks:
            self.get_or_create(task=task.name,
                               defaults=dict(content_type=ContentType.objects.get_for_model(task._model),
                                             timestamp=None,
                                             table_name=task._model._meta.db_table))


class TaskLog(models.Model):
    task = models.CharField(max_length=200, unique=True)
    timestamp = models.DateTimeField(null=True)
    result = models.CharField(max_length=200)
    elapsed = models.IntegerField(null=True)
    last_success = models.DateTimeField(null=True)
    last_failure = models.DateTimeField(null=True)
    table_name = models.CharField(max_length=200, null=True)
    content_type = models.ForeignKey(ContentType, models.CASCADE, null=True)

    objects = TaskLogManager()

    def __str__(self):
        return f"{self.task} {self.result}"
