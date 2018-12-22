# -*- coding: utf-8 -*-
import logging

from django.template import loader

from rest_framework.renderers import BrowsableAPIRenderer as _BrowsableAPIRenderer
from rest_framework.reverse import reverse

logger = logging.getLogger(__name__)


class URFBrowsableAPIRenderer(_BrowsableAPIRenderer):
    template = 'rest_framework/api.html'
    filter_template = 'rest_framework/filter_template.html'

    def get_filter_form(self, data, view, request):
        if not hasattr(view, 'get_queryset') or not hasattr(view, 'filter_backends'):
            return

        # Infer if this is a list view or not.
        paginator = getattr(view, 'paginator', None)
        if isinstance(data, list):
            pass
        elif paginator is not None and data is not None:
            try:
                paginator.get_results(data)
            except (TypeError, KeyError):
                return
        elif not isinstance(data, list):
            return

        queryset = view.get_queryset()
        elements = []
        for backend in view.get_filter_backends():
            if hasattr(backend, 'to_html'):
                html = backend().to_html(request, queryset, view)
                if html:
                    elements.append(html)

        if not elements:
            return

        template = loader.get_template(self.filter_template)
        context = {'elements': elements}
        return template.render(context)

    def get_context(self, data, accepted_media_type, renderer_context):
        ctx = super(URFBrowsableAPIRenderer, self).get_context(data, accepted_media_type, renderer_context)
        # in the real flow, this is added by the MultiTenant Middleware
        # but this function is called before the middleware system is involved
        request = ctx['request']
        view = ctx['view']
        for key, value in sorted(request.api_info.items()):
            if key not in ['cache-hit']:
                ctx['response_headers'][key] = request.api_info.str(key)
        # ctx['response_headers']['ordering'] = getattr(view, 'ordering_fields', '')
        ctx['response_headers']['serializers'] = ", ".join(getattr(view, 'serializers_fieldsets', {}).keys())
        # ctx['response_headers']['filters'] = getattr(view, 'filter_fields', '')

        ctx['extra_actions'] = view.get_extra_action_url_map()
        ctx['base_action'] = reverse(f'api:{view.basename}-list', args=['latest'])

        if request.user.is_staff:
            try:
                service = view.get_service()
                service_url = reverse(f'admin:unicef_rest_framework_service_change', args=[service.pk])
                ctx['service_url'] = service_url
                ctx['service'] = service
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
