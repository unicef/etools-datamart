from rest_framework import serializers


class EToolsSerializer(serializers.ModelSerializer):
    country_nane = serializers.ReadOnlyField(source='schema')
