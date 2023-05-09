from etools_datamart.api.endpoints import common
from etools_datamart.api.endpoints.common import APIReadOnlyModelViewSet
from etools_datamart.api.endpoints.etools import serializers
from etools_datamart.apps.mart.data.models import PartnersPlannedEngagement
from etools_datamart.apps.sources.etools import models

# class PartnerViewSet(common.APIMultiTenantReadOnlyModelViewSet):
#     serializer_class = serializers.PartnerSerializer
#     queryset = models.PartnersPartnerorganization.objects.all()


# class EtoolsAssessmentViewSet(common.APIMultiTenantReadOnlyModelViewSet):
#     serializer_class = serializers.AssessmentSerializer
#     queryset = models.PartnersAssessment.objects.all()


# class AgreementViewSet(common.APIMultiTenantReadOnlyModelViewSet):
#     serializer_class = serializers.AgreementSerializer
#     queryset = models.PartnersAgreement.objects.all()
#
#
# class PartnersInterventionViewSet(common.APIMultiTenantReadOnlyModelViewSet):
#     serializer_class = serializers.PartnersInterventionSerializer
#     queryset = models.PartnersIntervention.objects.all()


class EtoolsPlannedengagementViewSet(APIReadOnlyModelViewSet):
    serializer_class = serializers.PlannedengagementSerializer
    queryset = PartnersPlannedEngagement.objects.all()
