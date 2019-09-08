from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone

from crashlog.middleware import process_exception
from rest_framework.test import APIClient

from unicef_security.models import User

import etools_datamart


class Client(APIClient):
    def _base_environ(self, **request):
        env = super(Client, self)._base_environ(**request)
        env['HTTP_USER_AGENT'] = 'Datamart/%s' % etools_datamart.VERSION
        env['REMOTE_ADDR'] = '127.0.0.1'
        env['SERVER_NAME'] = 'localhost'
        env['SERVER_PORT'] = '80'
        return env


class Preload(models.Model):
    url = models.CharField(max_length=200)
    as_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    params = JSONField(blank=True, null=True, default=dict())
    enabled = models.BooleanField(default=True, blank=True)

    last_run = models.DateTimeField(blank=True, null=True)

    status_code = models.IntegerField(blank=True, null=True)
    response_length = models.IntegerField(blank=True, null=True)
    response_ms = models.PositiveIntegerField('ms', default=0, blank=True, null=True)

    class Meta:
        unique_together = ('url', 'as_user', 'params')
        ordering = ('url',)

    def run(self):
        try:
            self.last_run = timezone.now()
            target = "%s%s" % (settings.ABSOLUTE_BASE_URL, self.url)
            client = Client()
            if self.as_user:
                client.force_authenticate(self.as_user)
            response = client.get(target, )
            self.status_code = response.status_code
            self.response_length = len(response.content)
            response_timedelta = timezone.now() - self.last_run
            self.response_ms = int(response_timedelta.total_seconds() * 1000)
            return response
        except Exception as e:
            process_exception(e)
            raise
        finally:
            self.save()
