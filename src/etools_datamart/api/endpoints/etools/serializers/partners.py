from rest_framework import serializers

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
    partner = serializers.SerializerMethodField()
    vendor_number = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_partner_object(self, obj):
        return [
            partner
            for partner in PartnersPartnerorganization.objects.filter(pk=obj.partner_id)
            if partner.schema == obj.schema
        ][0]

    def get_partner(self, obj):
        return self.get_partner_object(obj).name

    def get_vendor_number(self, obj):
        return self.get_partner_object(obj).vendor_number

    def get_type(self, obj):
        return self.get_partner_object(obj).cso_type

    class Meta:
        model = models.PartnersPlannedengagement
        fields = "__all__"
