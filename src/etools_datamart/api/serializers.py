from rest_framework import serializers
from etools_datamart.apps.etools.models import *


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnersPartnerorganization
        exclude = ()


class ReportsResultSerializer(serializers.ModelSerializer):
    # result_type_name = serializers.CharField()
    class Meta:
        model = ReportsResult
        exclude = ()
