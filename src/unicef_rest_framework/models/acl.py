# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from .base import MasterDataModel
from .service import Service

logger = logging.getLogger(__name__)


class SerializerField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 200
        kwargs['name'] = 'serializer'
        super().__init__(*args, **kwargs)


def default_serializer():
    return ['std']


class AbstractAccessControl(MasterDataModel):
    service = models.ForeignKey(Service, models.CASCADE)
    rate = models.CharField(max_length=50)
    serializers = ArrayField(SerializerField(),
                             default=default_serializer,
                             blank=True)

    class Meta:
        abstract = True


# class ApplicationAccessControl(AbstractAccessControl):
#     application = models.ForeignKey(Application, related_name='acl')
#
#     class Meta:
#         verbose_name = 'Application ACL'
#         verbose_name_plural = 'Application ACLs'
#         ordering = ('application',)
#
#     def __unicode__(self):
#         return "{0.application} {0.service}".format(self)


class UserAccessControl(AbstractAccessControl):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='acl')

    class Meta:
        verbose_name = 'User ACL'
        verbose_name_plural = 'User ACLs'
        ordering = ('user',)
