from django.conf import settings
from django.db import models
from django.utils import timezone

from crashlog.middleware import process_exception
from django_extensions.db.fields.json import JSONField
from rest_framework.test import APIClient

from unicef_security.models import User


class Preload(models.Model):
    url = models.CharField(max_length=200)
    as_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    params = JSONField(blank=True, null=True, default=dict())
    enabled = models.BooleanField(default=True, blank=True)

    last_run = models.DateTimeField(blank=True, null=True)
    last_status_code = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('url', 'as_user', 'params')
        ordering = ('url',)

    def run(self):
        try:
            self.last_run = timezone.now()
            target = "%s%s" % (settings.ABSOLUTE_BASE_URL, self.url)
            client = APIClient()
            if self.as_user:
                client.force_authenticate(self.as_user)
            response = client.get(target)
            self.last_status_code = response.status_code
            return response
        except Exception as e:
            process_exception(e)
            raise
        finally:
            self.save()
