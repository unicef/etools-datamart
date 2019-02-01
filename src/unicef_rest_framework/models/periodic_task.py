from django_celery_beat import models

from unicef_rest_framework.models import Service


class PeriodicTask(models.PeriodicTask):
    service = models.models.ForeignKey(Service,
                                       on_delete=models.models.CASCADE,
                                       blank=True,
                                       null=True,
                                       related_name='periodic_tasks')
