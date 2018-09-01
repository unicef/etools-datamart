# -*- coding: utf-8 -*-
import logging

from drf_yasg.inspectors import CoreAPICompatInspector

logger = logging.getLogger(__name__)


class FilterInspector(CoreAPICompatInspector):
    def get_filter_parameters(self, filter_backend):
        ret = super(FilterInspector, self).get_filter_parameters(filter_backend)
        if hasattr(self.view, 'get_schema_fields'):
            ret += self.view.get_schema_fields()
        return ret
