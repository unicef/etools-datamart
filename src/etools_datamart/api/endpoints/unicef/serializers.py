from rest_framework import serializers
from unicef_realm import models


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        exclude = ()
