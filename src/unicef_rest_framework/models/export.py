import os
from io import BytesIO
from pathlib import Path
from urllib.parse import urlencode

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from unicef_rest_framework.storage import OverwriteStorage

from .preload import AbstractPreload, Client

FORMATS = (
    ('text/plain', 'txt'),
    ('text/csv', 'csv'),
    ('application/xlsx', 'xlsx'),
    ('application/json', 'json'),
)


def get_filename(instance, filename):
    return os.path.join(str(instance.as_user_id), filename)


class Export(AbstractPreload):
    name = models.CharField(max_length=100)
    format = models.CharField(max_length=30, choices=FORMATS)
    refresh = models.BooleanField(default=False, help_text='If true data are refreshed every day')
    filename = models.CharField(max_length=100,
                                help_text='Optional file name')
    save_as = models.BooleanField(default=False,
                                  help_text='If true, DataMart will try to force '
                                            '"SaveAs" popup. Note that popup will '
                                            'be displayed in any case if browser do not '
                                            'natively support requested format')

    class Meta:
        unique_together = ('url', 'as_user', 'params', 'format')
        ordering = ('name',)

    def __str__(self):
        return self.name

    @cached_property
    def stem(self):
        if self.format == 'text/plain':
            return 'txt'
        else:
            return self.format.split('/')[1]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.filename = Path(self.filename).with_suffix('.%s' % self.stem)
        super().save(force_insert, force_update, using, update_fields)

    def check_access(self, user):
        params = dict(self.params)
        params.update({'page_size': '1',
                       'format': self.stem})
        url = "{}{}?{}".format(settings.ABSOLUTE_BASE_URL, self.url, urlencode(params))
        client = Client()
        client.force_authenticate(user)
        response = client.get(url)
        return response.status_code in [200, 304]

    def run(self, target=None):
        params = dict(self.params)
        params.update({'page_size': '-1',
                       'format': self.stem})
        url = "{}{}?{}".format(settings.ABSOLUTE_BASE_URL, self.url, urlencode(params))
        response = super().run(url)
        if response.status_code == 200:
            filename = "{}.{}".format(self.etag, self.stem)
            storage = OverwriteStorage()
            storage.save(filename, BytesIO(response.content))
        return response
