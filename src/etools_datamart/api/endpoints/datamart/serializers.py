# -*- coding: utf-8 -*-
from rest_framework import serializers

from etools_datamart.apps.data import models


class DataMartSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('schema_name', )


class FAMIndicatorSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FAMIndicator
