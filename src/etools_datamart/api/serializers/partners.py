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


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnersAssessment
        exclude = ()


class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnersAgreement
        exclude = ()

#
# class PartnersInterventionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.PartnersIntervention
#         exclude = ()


class PlannedengagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnersPlannedengagement
        exclude = ()
