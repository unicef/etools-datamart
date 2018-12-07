# -*- coding: utf-8 -*-
from etools_datamart.api import serializers
from etools_datamart.api.endpoints import common
from etools_datamart.apps.etools import models


class EngagementViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.EngagementSerializer
    queryset = models.AuditEngagement.objects.all()
    filter_fields = ['joint_audit', 'status', 'engagement_type',
                     'cancel_comment']
