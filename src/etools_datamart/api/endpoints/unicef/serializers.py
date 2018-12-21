# -*- coding: utf-8 -*-
from rest_framework import serializers

from unicef_security import models


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        exclude = ()
