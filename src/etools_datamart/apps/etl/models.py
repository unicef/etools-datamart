from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import JSONField
from django.utils.functional import cached_property

from django_celery_beat.models import PeriodicTask
from picklefield import PickledObjectField

from etools_datamart.celery import app

from .loader import RUN_TYPES, RUN_UNKNOWN


class TaskLogManager(models.Manager):
    def filter_for_models(self, *models):
        return self.filter(content_type__in=ContentType.objects.get_for_models(*models).values())

    def get_for_model(self, model):
        try:
            return self.get(content_type=ContentType.objects.get_for_model(model))
        except EtlTask.MultipleObjectsReturned:  # pragma: no cover
            raise EtlTask.MultipleObjectsReturned(f"MultipleObjectsReturned for model '{model.__name__}'")
        except EtlTask.DoesNotExist:
            raise EtlTask.DoesNotExist(f"EtlTask for model '{model.__name__}' does not exists")

    def inspect(self):
        tasks = app.get_all_etls()
        results = {True: 0, False: 0}
        new = []
        for task in tasks:
            t, created = self.get_or_create(
                content_type=ContentType.objects.get_for_model(task.linked_model),
                defaults=dict(task=task.name, status="", last_run=None, table_name=task.linked_model._meta.db_table),
            )
            results[created] += 1
            new.append(t.id)
        self.exclude(id__in=new).delete()
        return {"created": results[True], "updated": results[False]}


class EtlTask(models.Model):
    STATUSES = (
        ("QUEUED", "QUEUED"),
        ("RUNNING", "RUNNING"),
        ("FAILURE", "FAILURE"),
        ("SUCCESS", "SUCCESS"),
        ("ERROR", "ERROR"),
        # ('NODATA', 'NO DATA'),
    )
    task = models.CharField(max_length=200, unique=True)
    task_id = models.CharField("UUID", blank=True, null=True, max_length=36, unique=True)
    last_run = models.DateTimeField(blank=True, null=True, help_text="last execution time")
    status = models.CharField(max_length=200, blank=True, null=True)
    elapsed = models.IntegerField(blank=True, null=True)
    run_type = models.IntegerField(choices=RUN_TYPES, default=RUN_UNKNOWN, blank=True)
    last_success = models.DateTimeField(null=True, blank=True, help_text="last successully execution time")
    last_failure = models.DateTimeField(null=True, blank=True, help_text="last failure execution time")
    last_changes = models.DateTimeField(null=True, blank=True, help_text="last time data have been changed")
    table_name = models.CharField(max_length=200, null=True)
    content_type = models.OneToOneField(ContentType, models.CASCADE, null=True)

    results = JSONField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)

    objects = TaskLogManager()

    class Meta:
        get_latest_by = "last_run"
        ordering = ("task",)

    def __str__(self):
        return f"{self.task} {self.status}"

    @cached_property
    def loader(self):
        return self.content_type.model_class().loader

    def update(self, **values):
        for attr, val in values.items():
            setattr(self, attr, val)
        self.save()

    update.alters_data = True

    @cached_property
    def verbose_name(self):
        return self.content_type.model_class()._meta.verbose_name

    @cached_property
    def periodic_task(self):
        try:
            return PeriodicTask.objects.get(task=self.task)
        except PeriodicTask.DoesNotExist:
            pass

    def snapshot(self):
        if self.status == "SUCCESS":
            return EtlTaskHistory.objects.create(
                task=self.task, timestamp=self.last_run, elapsed=self.elapsed, delta=None
            )


class EtlTaskHistory(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    task = models.CharField(max_length=200, db_index=True)
    elapsed = models.IntegerField(blank=True, null=True)
    delta = models.IntegerField(blank=True, null=True, default=None)
    delta_percentage = models.FloatField(blank=True, null=True, default=None)

    class Meta:
        get_latest_by = "last_run"
        ordering = ("-timestamp", "task")


class Config(models.Model):
    key = models.CharField(max_length=200, null=True, unique=True)
    value = PickledObjectField()
