from etools_datamart.apps.etools import models

from . import common
from .. import serializers


class PartnerViewSet(common.ReadOnlyModelViewSet):
    serializer_class = serializers.PartnerSerializer
    queryset = models.PartnersPartnerorganization.objects.all()


class AssessmentViewSet(common.ReadOnlyModelViewSet):
    serializer_class = serializers.AssessmentSerializer
    queryset = models.PartnersAssessment.objects.all()


class AgreementViewSet(common.ReadOnlyModelViewSet):
    serializer_class = serializers.AgreementSerializer
    queryset = models.PartnersAgreement.objects.all()


class InterventionViewSet(common.ReadOnlyModelViewSet):
    serializer_class = serializers.InterventionSerializer
    queryset = models.PartnersIntervention.objects.all()


class PlannedengagementViewSet(common.ReadOnlyModelViewSet):
    serializer_class = serializers.PlannedengagementSerializer
    queryset = models.PartnersPlannedengagement.objects.all()
