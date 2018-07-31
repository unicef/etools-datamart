from rest_framework import viewsets


class ApiMixin:
    permission_classes = []


class ReadOnlyModelViewSet(ApiMixin, viewsets.ReadOnlyModelViewSet):
    pass


class ModelViewSet(ApiMixin, viewsets.ReadOnlyModelViewSet):
    pass

# class PartnerViewSet(ReadOnlyModelViewSet):
#     serializer_class = PartnerSerializer
#     queryset = TpmpartnersTpmpartner.objects.all()
