# -*- coding: utf-8 -*-
from rest_framework import serializers

from etools_datamart.apps.sources.etools import models


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FundsGrant
        exclude = ()


class FundsreservationitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FundsFundsreservationitem
        exclude = ()


class FundsReservationHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FundsFundsreservationheader
        exclude = ()
