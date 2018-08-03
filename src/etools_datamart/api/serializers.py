from rest_framework import serializers
from etools_datamart.apps.etools import models


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnersPartnerorganization
        exclude = ()


class PK(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        if self.pk_field is not None:
            return self.pk_field.to_representation(value.pk)
        return value.pk


class ReportsResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReportsResult
        exclude = ()
