from rest_framework import serializers

from etools_datamart.apps.sources.etools.models import UsersCountry


class EToolsSerializer(serializers.ModelSerializer):
    country_name = serializers.ReadOnlyField(source="schema")


class CountrySerializerMixin(serializers.Serializer):
    country = serializers.SerializerMethodField()

    def get_country(self, obj):
        return getattr(UsersCountry.objects.filter(schema_name=obj.schema_name).first(), "name", None)
