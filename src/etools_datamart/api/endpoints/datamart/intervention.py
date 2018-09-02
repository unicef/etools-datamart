# -*- coding: utf-8 -*-
from etools_datamart.apps.data import models

from . import serializers
from .. import common


class InterventionViewSet(common.APIReadOnlyModelViewSet):
    """

    """
    serializer_class = serializers.InterventionSerializer
    queryset = models.Intervention.objects.all()
    filter_fields = ('country_name', 'title', 'status',
                     'start_date', 'submission_date',)
    serializers_fieldsets = {'std': None,
                             'short': ["title", "number"]}
