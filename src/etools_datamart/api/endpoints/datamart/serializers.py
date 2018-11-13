# -*- coding: utf-8 -*-
from datetime import datetime

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from etools_datamart.apps.data import models


class PMPIndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PMPIndicators
        exclude = ()


class InterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Intervention
        exclude = ()


class FAMIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FAMIndicator
        exclude = ()


class UserStatsSerializer(serializers.ModelSerializer):
    month = SerializerMethodField(help_text="---")

    class Meta:
        model = models.UserStats
        exclude = ()

    def get_month(self, obj):
        return datetime.strftime(obj.month._date, '%b %Y')


class HACTSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HACT
        exclude = ()
