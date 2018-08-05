from rest_framework import serializers

from etools_datamart.apps.etools import models


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnersPartnerorganization
        exclude = ()

class ReportsResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReportsResult
        exclude = ()
