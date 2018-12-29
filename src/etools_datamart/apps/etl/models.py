# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from django_celery_beat.models import PeriodicTask

from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.celery import app


class TaskLogManager(models.Manager):
    def filter_for_models(self, *models):
        return self.filter(content_type__in=ContentType.objects.get_for_models(*models).values())

    def get_for_model(self, model: DataMartModel):
        try:
            return self.get(content_type=ContentType.objects.get_for_model(model))
        except EtlTask.MultipleObjectsReturned:
            raise EtlTask.MultipleObjectsReturned(f"MultipleObjectsReturned for model '{model.__name__}'")
        except EtlTask.DoesNotExist:
            raise EtlTask.DoesNotExist(f"EtlTask for model '{model.__name__}' does not exists")

    def inspect(self):
        tasks = app.get_all_etls()
        results = {True: 0, False: 0}
        new = []
        for task in tasks:
            t, created = self.get_or_create(content_type=ContentType.objects.get_for_model(task.linked_model),
                                            defaults=dict(
                                                task=task.name,
                                                last_run=None,
                                                table_name=task.linked_model._meta.db_table))
            results[created] += 1
            new.append(t.id)
        self.exclude(id__in=new).delete()
        return {'created': results[True], 'updated': results[False]}


class EtlTask(models.Model):
    task = models.CharField(max_length=200, unique=True)
    last_run = models.DateTimeField(null=True, help_text="last execution time")
    status = models.CharField(max_length=200)
    elapsed = models.IntegerField(null=True)
    last_success = models.DateTimeField(null=True, help_text="last successully execution time")
    last_failure = models.DateTimeField(null=True, help_text="last failure execution time")
    last_changes = models.DateTimeField(null=True, help_text="last time data have been changed")
    table_name = models.CharField(max_length=200, null=True)
    content_type = models.OneToOneField(ContentType, models.CASCADE, null=True)

    results = JSONField(blank=True, null=True)

    objects = TaskLogManager()

    class Meta:
        get_latest_by = 'last_run'

    def __str__(self):
        return f"{self.task} {self.status}"

    @cached_property
    def loader(self):
        try:
            return self.content_type.model_class().loader
        except AttributeError:
            return None

    @cached_property
    def verbose_name(self):
        return self.content_type.model_class()._meta.verbose_name

    @cached_property
    def periodic_task(self):
        try:
            return PeriodicTask.objects.get(task=self.task)
        except PeriodicTask.DoesNotExist:
            pass
