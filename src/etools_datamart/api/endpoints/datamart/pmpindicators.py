# -*- coding: utf-8 -*-
from etools_datamart.apps.data import models

from . import serializers
from .. import common


class PMPIndicatorsViewSet(common.DataMartViewSet):
    serializer_class = serializers.PMPIndicatorsSerializer
    queryset = models.PMPIndicators.objects.all()
    filter_fields = ('partner_type', 'last_modify_date', 'pd_ssfa_status')
    serializers_fieldsets = {"std": None,
                             "brief": ["id", "country_name",
                                       "partner_name", "partner_type", "total_budget",
                                       "unicef_budget", "currency",
                                       ],
                             "ssfa": ["pd_ssfa_ref",
                                      "pd_ssfa_status",
                                      "pd_ssfa_start_date",
                                      "pd_ssfa_creation_date",
                                      "pd_ssfa_end_date"]}
