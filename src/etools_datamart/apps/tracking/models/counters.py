import logging

from django.conf import settings
from django.db import connections, models

from unicef_rest_framework.models import Service

logger = logging.getLogger(__name__)


class CounterManager(models.Manager):
    def truncate(self):
        conn = connections['default']
        cursor = conn.cursor()
        cursor.execute(f'TRUNCATE TABLE "{self.model._meta.db_table}"')


class AbstractCounter(models.Model):
    day = models.DateField(db_index=True)
    total = models.BigIntegerField(db_index=True)
    cached = models.BigIntegerField(db_index=True)
    response_max = models.BigIntegerField(db_index=True)
    response_min = models.BigIntegerField(db_index=True)
    response_average = models.FloatField(db_index=True)

    class Meta:
        abstract = True
        ordering = ('-day',)
        get_latest_by = 'day'

    objects = CounterManager()

    def __str__(self):
        return self.day.strftime('%d %b %Y')


class DailyCounter(AbstractCounter):
    users = models.IntegerField(db_index=True)


class MonthlyCounter(AbstractCounter):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                             blank=True, null=True)

    class Meta:
        unique_together = ('day', 'user')


class PathCounter(AbstractCounter):
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                blank=True, null=True)
    path = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = ('day', 'path')
        ordering = ('-day',)


class UserCounter(AbstractCounter):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                             blank=True, null=True)

    class Meta:
        unique_together = ('day', 'user')
