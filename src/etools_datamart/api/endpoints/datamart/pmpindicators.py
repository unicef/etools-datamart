# -*- coding: utf-8 -*-
from etools_datamart.apps.data import models

from . import serializers
from .. import common


class PMPIndicatorsViewSet(common.APIReadOnlyModelViewSet):
    """

    """
    serializer_class = serializers.PMPIndicatorsSerializer
    queryset = models.PMPIndicators.objects.all()
    filter_fields = ('country_name', 'business_area_code', 'vendor_number',
                     'partner_name', 'partner_type',
                     'pd_ssfa_ref', )
