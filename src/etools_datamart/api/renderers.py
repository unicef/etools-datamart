# -*- coding: utf-8 -*-
import logging

from unicef_rest_framework.renderers import APIBrowsableAPIRenderer as _BrowsableAPIRenderer

from etools_datamart.state import state

logger = logging.getLogger(__name__)


class APIBrowsableAPIRenderer(_BrowsableAPIRenderer):
    def get_context(self, data, accepted_media_type, renderer_context):
        ctx = super(APIBrowsableAPIRenderer, self).get_context(data, accepted_media_type, renderer_context)
        # in the real flow, this is added by the MultiTenant Middleware
        # but this function is called before the middleware system is involved

        # ctx['response_headers']['X-Schema'] = ",".join(state.schemas)
        # ctx['response_headers']['cache-version'] = str(state.get('cache-version'))
        # ctx['response_headers']['cache-key'] = str(state.get('cache-key'))
        ctx['response_headers']['system-filters'] = getattr(state.request, '_system_filter', '')

        return ctx
