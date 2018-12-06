# -*- coding: utf-8 -*-
from rest_framework import serializers
from unicef_security import models


class BusinessAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BusinessArea
        exclude = ('country',)


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        exclude = ()
