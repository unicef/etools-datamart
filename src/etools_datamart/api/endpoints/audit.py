# -*- coding: utf-8 -*-
from etools_datamart.apps.etools import models

from . import common
from .. import serializers


class EngagementViewSet(common.ReadOnlyModelViewSet):
    serializer_class = serializers.EngagementSerializer
    queryset = models.AuditEngagement.objects.all()
