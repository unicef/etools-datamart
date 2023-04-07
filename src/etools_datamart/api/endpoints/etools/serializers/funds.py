from rest_framework import serializers

from etools_datamart.apps.sources.etools import models
from etools_datamart.apps.sources.etools.models import UsersCountry


class EToolsGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FundsGrant
        exclude = ()


class EToolsFundsreservationitemSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()

    def get_country_name(self, obj):
        return getattr(UsersCountry.objects.filter(schema_name=obj.schema).first(), "name", None)

    class Meta:
        model = models.FundsFundsreservationitem
        fields = "__all__"


class EToolsFundsReservationHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FundsFundsreservationheader
        exclude = ()
