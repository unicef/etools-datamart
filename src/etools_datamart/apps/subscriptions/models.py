import logging
from io import BytesIO

from crashlog.middleware import process_exception
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property
from post_office import mail
from rest_framework.test import APIRequestFactory
from unicef_rest_framework.models import Service

from etools_datamart.apps.etl.models import EtlTask

logger = logging.getLogger(__name__)


class SubscriptionManager(models.Manager):
    def notify(self, model):
        ct = ContentType.objects.get_for_model(model)
        etl = EtlTask.objects.filter(content_type=ct).first()
        service = Service.objects.get(source_model=ct)
        ret = []
        for subscription in self.filter(content_type=ct).exclude(type=Subscription.NONE):
            logger.info(f"Process subscription {subscription}")
            try:
                if subscription.type in (Subscription.EXCEL, Subscription.PDF):
                    format = {Subscription.EXCEL: 'xlsx',
                              Subscription.PDF: 'pdf',
                              }[subscription.type]
                    rf = APIRequestFactory()
                    request = rf.get(f"{service.endpoint}?format={format}")
                    request.user = subscription.user
                    request.api_info = {}  # this is set my the middleware, so we must set manually here
                    response = service.viewset.as_view({'get': 'list'})(request)
                    response.render()

                    # check headers set in ApiMiddleware in request.api_info
                    request.api_info.update(dict(response.items()))

                    attachments = {
                        f'{model._meta.verbose_name}.{format}': BytesIO(response.content),
                    }
                    template = 'dataset_changed_attachment'
                else:
                    attachments = None
                    template = 'dataset_changed'

                ret.append(mail.send(
                    subscription.user.email,  # List of email addresses also accepted
                    'notification@datamart.unicef.io',
                    template=template,
                    context={'subscription': subscription,
                             'user': subscription.user,
                             'base_url': settings.ABSOLUTE_BASE_URL,
                             'verbose_name': model._meta.verbose_name,
                             'etl': etl,
                             'model': ct.model,
                             'service': service
                             },
                    attachments=attachments
                ))
            except Exception as e:  # pragma: no cover
                logger.exception(e)
                process_exception(e)
        return ret


class Subscription(models.Model):
    NONE = 0
    MESSAGE = 1
    EXCEL = 2
    PDF = 3

    TYPES = ((NONE, 'None'),
             (MESSAGE, 'Email'),
             (EXCEL, 'Email+Excel'),
             (PDF, 'Email+Pdf'),
             )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                             related_name='subscriptions')
    type = models.IntegerField(choices=TYPES)
    content_type = models.ForeignKey(ContentType, models.CASCADE)
    kwargs = models.CharField(max_length=500, blank=True, null=False, default='')
    last_notification = models.DateField(blank=True, null=True)

    objects = SubscriptionManager()

    class Meta:
        unique_together = ('user', 'content_type', 'kwargs')

    def __str__(self):
        return f"#{self.pk} {self.user} {self.get_type_display()} {self.content_type}"

    # @cached_property
    # def endpoint(self):
    #     return self.content_type.model_class().service.endpoint
    #
    # @cached_property
    # def service(self):
    #     return self.content_type.model_class().service

    @cached_property
    def viewset(self):
        return self.content_type.model_class().service.viewset
