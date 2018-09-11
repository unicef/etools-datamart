# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Model

from etools_datamart.celery import app, ETLTask


class TaskLogManager(models.Manager):
    def get_for_model(self, model: Model):
        return self.get(content_type=ContentType.objects.get_for_model(model))

    def get_for_task(self, task: ETLTask):
        return self.get_or_create(task=task.name,
                                  defaults=dict(content_type=ContentType.objects.get_for_model(task.linked_model),
                                                timestamp=None,
                                                table_name=task.linked_model._meta.db_table))[0]

    def inspect(self):
        tasks = [cls for (name, cls) in app.tasks.items() if name.startswith('etl_')]
        results = {True: 0, False: 0}
        for task in tasks:
            __, created = self.get_or_create(task=task.name,
                                             defaults=dict(
                                                 content_type=ContentType.objects.get_for_model(task.linked_model),
                                                 timestamp=None,
                                                 table_name=task.linked_model._meta.db_table))
            results[created] += 1
        return results[True], results[False]


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
