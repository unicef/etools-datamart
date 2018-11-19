# -*- coding: utf-8 -*-
from rest_framework import serializers

from etools_datamart.apps.etl import models


class TaskLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EtlTask
        exclude = ('content_type', 'id')
