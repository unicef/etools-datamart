from unicef_rest_framework.ds import DynamicSerializerFilter
from unicef_rest_framework.ordering import OrderingFilter

from etools_datamart.api.endpoints.common import DataMartViewSet
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.api.filtering import DatamartQueryStringFilterBackend
from etools_datamart.apps.mart.unpp import models


class ApplicationSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Application
        exclude = None
        fields = '__all__'


class ApplicationViewSet(DataMartViewSet):
    serializer_class = ApplicationSerializer
    queryset = models.Application.objects.all()
    serializers_fieldsets = {'std': ApplicationSerializer, }
    filter_backends = [
        DatamartQueryStringFilterBackend,
        OrderingFilter,
        DynamicSerializerFilter,
    ]
