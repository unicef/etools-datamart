import logging

from django.conf import settings
from django.template import loader

from rest_framework.renderers import BaseRenderer

from unicef_rest_framework.renderers.mixin import ContentDispositionMixin
from unicef_rest_framework.utils import get_query_string

logger = logging.getLogger(__name__)


def labelize(v):
    return v.replace("_", " ").title()


class IQYRenderer(ContentDispositionMixin, BaseRenderer):
    media_type = "text/plain"
    format = "iqy"
    charset = "utf-8"
    render_style = "text"

    def get_template(self, meta):
        return loader.select_template(
            [
                f"renderers/iqy/{meta.app_label}/{meta.model_name}.txt",
                f"renderers/iqy/{meta.app_label}/iqy.txt",
                "renderers/iqy.txt",
            ]
        )

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context["response"]
        request = renderer_context["request"]
        # view = renderer_context['view']
        # try:
        #     filename = view.get_service().name
        # except Exception:
        #     filename = self.__class__.__name__
        # response['Content-Disposition'] = u'attachment; filename="%s.iqy"' % filename
        self.process_response(renderer_context)
        if response.status_code != 200:
            return ""
        try:
            qs = get_query_string(request.query_params, {"format": "iqy"}, remove=["format", "_display"])
            url = f"{request.path}".replace("/iqy/", "/")

            c = dict(host=settings.ABSOLUTE_BASE_URL, request=request, qs=qs, url=url)
            model = renderer_context["view"].queryset.model
            opts = model._meta
            template = self.get_template(opts)
            return template.render(c)
        except Exception as e:
            logger.exception(e)
            raise Exception("Error processing request %s" % e) from e
