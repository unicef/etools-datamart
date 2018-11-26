# -*- coding: utf-8 -*-
from rest_framework import serializers

from etools_datamart.apps.etools import models


class EngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuditEngagement
        exclude = ()

    def fail(self, key, **kwargs):
        return super().fail(key, **kwargs)
