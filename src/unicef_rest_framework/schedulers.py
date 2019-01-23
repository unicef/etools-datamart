from django_celery_beat import schedulers

from unicef_rest_framework.models.periodic_task import PeriodicTask


class DatabaseScheduler(schedulers.DatabaseScheduler):
    Model = PeriodicTask
