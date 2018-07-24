from rest_framework import viewsets

from etools_datamart.api.serializers import PartnerSerializer
# from etools_datamart.apps.etools.public.models import TpmpartnersTpmpartner


class ApiMixin:
    permission_classes = []


class ReadOnlyModelViewSet(ApiMixin, viewsets.ReadOnlyModelViewSet):
    pass


class ModelViewSet(ApiMixin, viewsets.ReadOnlyModelViewSet):
    pass


# class PartnerViewSet(ReadOnlyModelViewSet):
#     serializer_class = PartnerSerializer
#     queryset = TpmpartnersTpmpartner.objects.all()
