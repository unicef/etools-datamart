from crashlog.middleware import process_exception
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from post_office import mail
from unicef_rest_framework.models import Service

from etools_datamart.apps.etl.models import EtlTask


class SubscriptionManager(models.Manager):
    def notify(self, model):
        ct = ContentType.objects.get_for_model(model)
        etl = EtlTask.objects.filter(content_type=ct).first()

        for subscription in self.filter(content_type=ct).exclude(type=Subscription.NONE):
            try:
                mail.send(
                    subscription.user.email,  # List of email addresses also accepted
                    'notification@datamart.unicef.io',
                    template='dataset_changed',  # Could be an EmailTemplate instance or name
                    context={'subscription': subscription,
                             'user': subscription.user,
                             'base_url': settings.ABSOLUTE_BASE_URL,
                             'verbose_name': model._meta.verbose_name,
                             'etl': etl,
                             'model': ct.model,
                             'service': Service.objects.get(source_model=ct)
                             },
                )
            except Exception as e:
                process_exception(e)


class Subscription(models.Model):
    NONE = 0
    MESSAGE = 1
    EXCEL = 2

    TYPES = ((NONE, 'None'),
             (MESSAGE, 'Email'),
             # (EXCEL, 'Email+Excel'),
             )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                             related_name='subscriptions')
    type = models.IntegerField(choices=TYPES)
    content_type = models.ForeignKey(ContentType, models.CASCADE)
    kwargs = models.CharField(max_length=500, blank=True, null=False, default='')

    objects = SubscriptionManager()

    class Meta:
        unique_together = ('user', 'content_type', 'kwargs')

    def __str__(self):
        return f"{self.user} {self.get_type_display()}"
