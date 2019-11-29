from urllib.parse import urlencode

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from crashlog.middleware import process_exception
from rest_framework.test import APIClient, ForceAuthClientHandler

from unicef_security.models import User

import etools_datamart


class ClientHandler(ForceAuthClientHandler):
    def get_response(self, request):
        request._is_preload_internal_request = True
        return super(ClientHandler, self).get_response(request)


class Client(APIClient):
    def __init__(self, enforce_csrf_checks=False, **defaults):
        super().__init__(**defaults)
        self.handler = ClientHandler(enforce_csrf_checks)
        self._credentials = {}

    def _base_environ(self, **request):
        env = super(Client, self)._base_environ(**request)
        env['HTTP_USER_AGENT'] = 'Datamart/%s' % etools_datamart.VERSION
        env['REMOTE_ADDR'] = '127.0.0.1'
        env['SERVER_NAME'] = 'localhost'
        env['SERVER_PORT'] = '80'
        env['HTTP_PAGINATION_KEY'] = settings.DISABLE_PAGINATION_KEY
        return env

    def request(self, **kwargs):
        request = super().request(**kwargs)
        return request


class AbstractPreload(models.Model):
    url = models.CharField(max_length=200)
    as_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    params = JSONField(blank=True, null=True, default=dict)
    enabled = models.BooleanField(default=True, blank=True)

    last_run = models.DateTimeField(blank=True, null=True)

    status_code = models.IntegerField(blank=True, null=True)
    response_length = models.IntegerField(blank=True, null=True)
    response_ms = models.PositiveIntegerField('ms', default=0, blank=True, null=True)
    etag = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        unique_together = ('url', 'as_user', 'params')
        ordering = ('url',)
        abstract = True

    def clean(self):
        super().clean()
        self.check_url(True)

    def get_full_url(self):
        return "%s%s?%s" % (settings.ABSOLUTE_BASE_URL, self.url,
                            urlencode(self.params))

    def check_url(self, validate=True):
        try:
            target = "%s%s" % (settings.ABSOLUTE_BASE_URL, self.url)
            client = Client()
            if self.as_user:
                client.force_authenticate(self.as_user)
            params = dict(self.params)
            params['page_size'] = 10
            res = client.head(target, data=params)
            if res.status_code != 200:
                raise Exception('Invalid Response: %s on %s' % (res.status_code,
                                                                self.get_full_url()))
        except Exception as e:
            if validate:
                raise ValidationError(str(e))
            else:
                return False

    def get_client(self, **kwargs):
        return Client(HTTP_IF_NONE_MATCH=self.etag or 'Not-Set', **kwargs)

    def run(self, *, target=None, params=None, pre_save=None):
        try:
            self.last_run = timezone.now()
            target = target or "%s%s" % (settings.ABSOLUTE_BASE_URL, self.url)
            client = self.get_client()
            if self.as_user:
                client.force_authenticate(self.as_user)
            params = params or self.params
            response = client.get(target, data=params)
            self.status_code = response.status_code
            if self.status_code == 200:
                self.response_length = len(response.content)
                self.etag = response['ETag']
                response_timedelta = timezone.now() - self.last_run
                self.response_ms = int(response_timedelta.total_seconds() * 1000)
            if pre_save:
                pre_save(self, response)
            return response
        except Exception as e:
            process_exception(e)
            self.status_code = 501
            self.etag = ""
            self.response_ms = 0
            raise
        finally:
            self.save()


class Preload(AbstractPreload):
    class Meta:
        pass
