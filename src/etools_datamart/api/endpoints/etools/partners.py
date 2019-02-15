from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.etools import serializers
from etools_datamart.apps.etools import models

# class PartnerViewSet(common.APIMultiTenantReadOnlyModelViewSet):
#     serializer_class = serializers.PartnerSerializer
#     queryset = models.PartnersPartnerorganization.objects.all()


class AssessmentViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.AssessmentSerializer
    queryset = models.PartnersAssessment.objects.all()


class AgreementViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.AgreementSerializer
    queryset = models.PartnersAgreement.objects.all()

#
# class PartnersInterventionViewSet(common.APIMultiTenantReadOnlyModelViewSet):
#     serializer_class = serializers.PartnersInterventionSerializer
#     queryset = models.PartnersIntervention.objects.all()


class PlannedengagementViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.PlannedengagementSerializer
    queryset = models.PartnersPlannedengagement.objects.all()
