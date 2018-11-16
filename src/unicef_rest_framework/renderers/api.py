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
        for key, value in request.api_info.items():
            ctx['response_headers'][key] = request.api_info.str(key)

        if request.user.is_staff:
            try:
                model = ctx['view'].queryset.model
                admin_url = reverse(f'admin:{model._meta.app_label}_{model._meta.model_name}_changelist')
                ctx['admin_url'] = admin_url
            except Exception:  # pragma: no cover
                pass
        return ctx
