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
        view = ctx['view']
        for key, value in sorted(request.api_info.items()):
            if key not in ['cache-hit']:
                ctx['response_headers'][key] = request.api_info.str(key)

        ctx['extra_actions'] = view.get_extra_action_url_map()
        ctx['base_action'] = reverse(f'api:{view.basename}-list', args=['latest'])

        if request.user.is_staff:
            try:
                service = view.get_service()
                service_url = reverse(f'admin:unicef_rest_framework_service_change', args=[service.pk])
                ctx['service_url'] = service_url
            except Exception:  # pragma: no cover
                pass
            try:
                model = ctx['view'].queryset.model
                # model = service.managed_model
                admin_url = reverse(f'admin:{model._meta.app_label}_{model._meta.model_name}_changelist')
                ctx['admin_url'] = admin_url
            except Exception:  # pragma: no cover
                pass

        try:
            ctx['iqy_url'] = ctx['extra_actions'].pop('Iqy')
        except Exception:  # pragma: no cover
            pass
        return ctx
