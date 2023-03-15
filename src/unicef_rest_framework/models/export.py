import os
from io import BytesIO
from pathlib import Path
from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.html import strip_tags

from strategy_field.utils import import_by_name

from .preload import AbstractPreload, Client

FORMATS = (
    ('text/plain', 'txt'),
    ('text/csv', 'csv'),
    ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'xlsx'),
    ('application/json', 'json'),
)


def get_filename(instance, filename):
    return os.path.join(str(instance.as_user_id), filename)


class Export(AbstractPreload):
    name = models.CharField(max_length=100)
    format = models.CharField(max_length=100, choices=FORMATS)
    refresh = models.BooleanField(default=False, help_text='If true data are refreshed every day')
    enabled = models.BooleanField(default=False, blank=True)
    filename = models.CharField(max_length=100,
                                help_text='Optional file name')
    save_as = models.BooleanField(default=False,
                                  help_text='If true, DataMart will try to force '
                                            '"SaveAs" popup. Note that popup will '
                                            'be displayed in any case if browser do not '
                                            'natively support requested format')
    notify = models.BooleanField(default=False,
                                 help_text='Send me an email when file is available')

    class Meta:
        unique_together = ('url', 'as_user', 'params', 'format')
        ordering = ('name',)

    def __str__(self):
        return self.name

    @cached_property
    def stem(self):
        if self.format == 'text/plain':
            return 'txt'
        elif self.format == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            return 'xlsx'
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

    def check_file(self):
        return storage.exists(self.file_id)

    @property
    def file_id(self):
        return "{}.{}".format(self.etag, self.stem)

    def get_client(self, **kwargs):
        return Client(HTTP_IF_NONE_MATCH=self.etag or 'Not-Set',
                      HTTP_PAGINATION_KEY=settings.API_PAGINATION_OVERRIDE_KEY,
                      **kwargs)

    def run(self, *, target=None, params=None, pre_save=None):
        def save_file(me, response):
            if me.status_code == 200:
                storage.save(self.file_id, BytesIO(response.content))

        params = dict(self.params)
        params.update({'page_size': '-1',
                       'format': self.stem})
        url = "{}{}".format(settings.ABSOLUTE_BASE_URL, self.url)
        response = super().run(target=url, params=params, pre_save=save_file)
        return response


@receiver(post_save, sender=Export)
def notify_new_export(sender, instance, created, **kwargs):
    if created and settings.ADMIN_EMAILS:
        admin_link = reverse('admin:%s_%s_change' % (instance._meta.app_label, instance._meta.model_name),
                             args=[instance.pk, ])
        subject = 'New Export {} {}'.format(instance.name, instance.format)
        html_message = f'{instance.as_user} requested a new export: ' \
                       f'<a href=https://datamart.unicef.io{admin_link}>{instance.name}</a>.'
        plain_message = strip_tags(html_message)
        from_email = getattr(instance.as_user, 'email', 'datamart@unicef.org')
        send_mail(subject, plain_message, from_email, settings.ADMIN_EMAILS, html_message=html_message)


def get_storage():
    storage_class = import_by_name(settings.EXPORT_FILE_STORAGE)
    return storage_class(**settings.EXPORT_FILE_STORAGE_KWARGS)


storage = get_storage()
