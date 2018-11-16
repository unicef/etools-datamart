# -*- coding: utf-8 -*-
import logging

from rest_framework.renderers import BrowsableAPIRenderer as _BrowsableAPIRenderer
from rest_framework.reverse import reverse

logger = logging.getLogger(__name__)


class APIBrowsableAPIRenderer(_BrowsableAPIRenderer):
    template = 'rest_framework/api.html'

    def get_context(self, data, accepted_media_type, renderer_context):
        ctx = super(APIBrowsableAPIRenderer, self).get_context(data, accepted_media_type, renderer_context)
        # in the real flow, this is added by the MultiTenant Middleware
        # but this function is called before the middleware system is involved
        request = ctx['request']

        # ctx['response_headers']['X-Schema'] = ",".join(state.schemas)
        ctx['response_headers']['cache-version'] = getattr(request, 'cache-version', '')
        ctx['response_headers']['cache-key'] = getattr(request, 'cache-key', '')
        ctx['response_headers']['system-filters'] = getattr(request, '_system_filter', '')
        ctx['response_headers']['filters'] = getattr(request, 'filters', '')
        ctx['response_headers']['excludes'] = getattr(request, 'excludes', '')

        if request.user.is_staff:
            try:
                model = ctx['view'].queryset.model
                admin_url = reverse(f'admin:{model._meta.app_label}_{model._meta.model_name}_changelist')
                ctx['admin_url'] = admin_url
            except Exception:  # pragma: no cover
                pass
        return ctx
