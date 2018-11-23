# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Model
from django.utils.functional import cached_property
from django_celery_beat.models import PeriodicTask

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
        tasks = app.get_all_etls()
        results = {True: 0, False: 0}
        new = []
        for task in tasks:
            t, created = self.get_or_create(task=task.name,
                                            defaults=dict(
                                                content_type=ContentType.objects.get_for_model(task.linked_model),
                                                timestamp=None,
                                                table_name=task.linked_model._meta.db_table))
            results[created] += 1
            new.append(t.id)
        self.exclude(id__in=new).delete()
        return results[True], results[False]


class EtlTask(models.Model):
    task = models.CharField(max_length=200, unique=True)
    timestamp = models.DateTimeField(null=True)
    status = models.CharField(max_length=200)
    elapsed = models.IntegerField(null=True)
    last_success = models.DateTimeField(null=True)
    last_failure = models.DateTimeField(null=True)
    table_name = models.CharField(max_length=200, null=True)
    content_type = models.ForeignKey(ContentType, models.CASCADE, null=True)

    results = JSONField(blank=True, null=True)

    objects = TaskLogManager()

    class Meta:
        get_latest_by = 'timestamp'

    def __str__(self):
        return f"{self.task} {self.status}"

    @cached_property
    def verbose_name(self):
        return self.content_type.model_class()._meta.verbose_name

    @cached_property
    def periodic_task(self):
        try:
            return PeriodicTask.objects.get(task=self.task)
        except PeriodicTask.DoesNotExist:
            pass
