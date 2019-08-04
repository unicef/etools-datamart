# -*- coding: utf-8 -*-
from rest_framework import serializers

from etools_datamart.apps.data import models


class DataMartSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('schema_name', )


class PMPIndicatorsSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.PMPIndicators


class FAMIndicatorSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FAMIndicator
