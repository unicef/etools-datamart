# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

from etools_datamart.api.urls import router

from .service import Service

logger = logging.getLogger(__name__)


class EndpointField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        kwargs['choices'] = [(url.name, url.name) for url in router.urls]
        super().__init__(*args, **kwargs)

    def get_choices(self, *args, **kwargs):
        return [url.name for url in router.urls]


class Authorization(models.Model):
    POLICY_FORBID = 0
    POLICY_GRANT = 1
    POLICY_DEFAULT = 2

    POLICIES = ((POLICY_FORBID, "Forbid"),
                (POLICY_GRANT, "Grant"),
                (POLICY_DEFAULT, "Default"),
                )
    service = models.ForeignKey(Service, models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    group = models.ForeignKey(Group, models.CASCADE)
    policy = models.IntegerField(choices=POLICIES)
