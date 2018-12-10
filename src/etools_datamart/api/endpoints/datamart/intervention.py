# -*- coding: utf-8 -*-
# import django_filters
from django_filters import rest_framework as filters

from etools_datamart.apps.data import models

from . import serializers
from .. import common


class InterventionFilter(filters.FilterSet):
    class Meta:
        model = models.Intervention
        fields = {
            'country_name': ['icontains', ],
            'title': ['icontains', ],
            'status': ['exact'],
            'start_date': ['exact', 'lt', 'gt'],
            'submission_date': ['exact', 'lt', 'gt'],
            'document_type': ['exact'],
        }
        # filter_overrides = {
        #     models.CharField: {
        #         'filter_class': django_filters.CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },
        #     models.BooleanField: {
        #         'filter_class': django_filters.BooleanFilter,
        #         'extra': lambda f: {
        #             'widget': forms.CheckboxInput,
        #         },
        #     },
        # }


class InterventionViewSet(common.DataMartViewSet):
    """

    """
    serializer_class = serializers.InterventionSerializer
    queryset = models.Intervention.objects.all()
    filter_fields = ('country_name', 'title', 'status', 'last_modify_date',
                     'start_date', 'submission_date', 'document_type')
    serializers_fieldsets = {'std': None,
                             'short': ["title", "number", "country_name", "start_date"]}
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_fields = ('category', 'in_stock')
    # filterset_class = InterventionFilter

    def get_schema_fields(self):
        return super().get_schema_fields()
