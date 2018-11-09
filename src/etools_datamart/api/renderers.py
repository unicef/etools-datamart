# -*- coding: utf-8 -*-
import logging

from django.urls import reverse
from rest_framework_csv import renderers as r
from unicef_rest_framework.renderers import APIBrowsableAPIRenderer as _BrowsableAPIRenderer

from etools_datamart.state import state

logger = logging.getLogger(__name__)


class APIBrowsableAPIRenderer(_BrowsableAPIRenderer):
    def get_context(self, data, accepted_media_type, renderer_context):
        ctx = super(APIBrowsableAPIRenderer, self).get_context(data, accepted_media_type, renderer_context)
        # in the real flow, this is added by the MultiTenant Middleware
        # but this function is called before the middleware system is involved

        # ctx['response_headers']['X-Schema'] = ",".join(state.schemas)
        ctx['response_headers']['cache-version'] = str(state.get('cache-version'))
        ctx['response_headers']['cache-key'] = str(state.get('cache-key'))
        ctx['response_headers']['system-filters'] = getattr(state.request, '_system_filter', '')
        ctx['response_headers']['filters'] = state.get('filters', '')
        ctx['response_headers']['excludes'] = state.get('excludes', '')

        request = ctx['request']
        if request.user.is_staff:
            try:
                model = ctx['view'].queryset.model
                admin_url = reverse(f'admin:{model._meta.app_label}_{model._meta.model_name}_changelist')
                ctx['admin_url'] = admin_url
            except Exception:  # pragma: no cover
                pass
        return ctx


class CSVRenderer(r.CSVRenderer):

    def render(self, data, media_type=None, renderer_context={}, writer_opts=None):
        data = dict(data)['results']
        return super().render(data, media_type, renderer_context, writer_opts)
