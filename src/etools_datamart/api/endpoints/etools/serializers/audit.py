# -*- coding: utf-8 -*-

from etools_datamart.apps.etools import models

from .base import EToolsSerializer


class EngagementSerializer(EToolsSerializer):
    class Meta:
        model = models.AuditEngagement
        exclude = ()
