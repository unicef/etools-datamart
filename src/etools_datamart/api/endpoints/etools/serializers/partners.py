from rest_framework import serializers

from etools_datamart.apps.mart.data.models import PartnersPlannedEngagement
from etools_datamart.apps.sources.etools import models
from etools_datamart.apps.sources.etools.models import PartnersPartnerorganization

from .base import EToolsSerializer

#
# class PartnerSerializer(EToolsSerializer):
#     class Meta:
#         model = models.PartnersPartnerorganization
#         exclude = ()


class ReportsResultSerializer(EToolsSerializer):
    class Meta:
        model = models.ReportsResult
        exclude = ()


class AssessmentSerializer(EToolsSerializer):
    class Meta:
        model = models.PartnersAssessment
        exclude = ()


# class AgreementSerializer(EToolsSerializer):
#     class Meta:
#         model = models.PartnersAgreement
#         exclude = ()
#
#
# class PartnersInterventionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.PartnersIntervention
#         exclude = ()


class PlannedengagementSerializer(EToolsSerializer):
    class Meta:
        model = PartnersPlannedEngagement
        fields = "__all__"
