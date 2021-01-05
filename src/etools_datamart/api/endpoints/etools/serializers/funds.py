from rest_framework import serializers

from etools_datamart.apps.sources.etools import models


class EToolsGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FundsGrant
        exclude = ()


class EToolsFundsreservationitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FundsFundsreservationitem
        exclude = ()


class EToolsFundsReservationHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FundsFundsreservationheader
        exclude = ()
