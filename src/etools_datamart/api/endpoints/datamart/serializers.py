# -*- coding: utf-8 -*-
from rest_framework import serializers

from etools_datamart.apps.data import models


class PMPIndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PMPIndicators
        exclude = ()


class InterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Intervention
        exclude = ()
