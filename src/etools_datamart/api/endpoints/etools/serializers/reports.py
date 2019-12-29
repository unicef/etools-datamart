from etools_datamart.apps.sources.etools import models

from .base import EToolsSerializer


class PartnerSerializer(EToolsSerializer):
    class Meta:
        model = models.PartnersPartnerorganization
        exclude = ()


class ReportsResultSerializer(EToolsSerializer):
    class Meta:
        model = models.ReportsResult
        exclude = ()


class AppliedindicatorSerializer(EToolsSerializer):
    class Meta:
        model = models.ReportsAppliedindicator
        exclude = ()
