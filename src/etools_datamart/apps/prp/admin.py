# -*- coding: utf-8 -*-
import logging

from django.contrib.admin import ModelAdmin, register

from etools_datamart.libs.truncate import TruncateTableMixin

from . import models

logger = logging.getLogger(__name__)


@register(models.IndicatorByLocation)
class IndicatorByLocationAdmin(TruncateTableMixin, ModelAdmin):
    list_display = ('source_id', 'project',
                    'country', 'partner', 'reference_number', 'title_of_indicator')
