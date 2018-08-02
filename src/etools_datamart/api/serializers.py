from rest_framework import serializers
from etools_datamart.apps.etools.models import *


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnersPartnerorganization
        exclude = ()


class PK(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        # FIXME: remove this line (pdb)
        import pdb; pdb.set_trace()
        if self.pk_field is not None:
            return self.pk_field.to_representation(value.pk)
        return value.pk


class ReportsResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportsResult
        exclude = ()
