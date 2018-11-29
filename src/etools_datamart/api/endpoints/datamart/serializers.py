# -*- coding: utf-8 -*-
from datetime import datetime

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from etools_datamart.apps.data import models


class DataMartSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('schema_name',)


class PMPIndicatorsSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.PMPIndicators


class InterventionSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Intervention


class FAMIndicatorSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.FAMIndicator


class UserStatsSerializer(DataMartSerializer):
    month = SerializerMethodField(help_text="---")

    class Meta(DataMartSerializer.Meta):
        model = models.UserStats
        read_only = ['last_modify_date', ]

    def get_month(self, obj):
        return datetime.strftime(obj.month._date, '%b %Y')


class HACTSerializer(DataMartSerializer):
    # last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    class Meta(DataMartSerializer.Meta):
        model = models.HACT
