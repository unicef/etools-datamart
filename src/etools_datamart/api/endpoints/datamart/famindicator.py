# -*- coding: utf-8 -*-
from month_field.rest_framework import MonthFilterBackend

from etools_datamart.apps.data import models

from . import serializers
from .. import common


class FAMIndicatorViewSet(common.DataMartViewSet):
    serializer_class = serializers.FAMIndicatorSerializer
    queryset = models.FAMIndicator.objects.all()
    filter_fields = ('last_modify_date', )
    filter_backends = [MonthFilterBackend] + common.APIReadOnlyModelViewSet.filter_backends
    serializers_fieldsets = {"std": None,
                             "spotcheck": ["country_name", "month", "spotcheck_ip_contacted",
                                           "spotcheck_report_submitted",
                                           "spotcheck_final_report",
                                           "spotcheck_cancelled"],
                             "audit": ["country_name", "month",
                                       "audit_ip_contacted", "audit_report_submitted",
                                       "audit_final_report",
                                       "audit_cancelled"],
                             "specialaudit": ["country_name", "month",
                                              "specialaudit_ip_contacted",
                                              "specialaudit_report_submitted",
                                              "specialaudit_final_report",
                                              "specialaudit_cancelled"],
                             "microassessment": ["country_name", "month",
                                                 "microassessment_ip_contacted",
                                                 "microassessment_report_submitted",
                                                 "microassessment_final_report",
                                                 "microassessment_cancelled"]
                             }
