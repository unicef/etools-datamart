# -*- coding: utf-8 -*-
from rest_framework import serializers

from etools_datamart.apps.etools import models


class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.T2FTravel
        exclude = ()
