import logging

from crashlog.middleware import process_exception
from django.template import loader
from rest_framework.renderers import BaseRenderer

logger = logging.getLogger(__name__)


def labelize(v):
    return v.replace("_", " ").title()


class HTMLRenderer(BaseRenderer):
    media_type = 'text/html'
    format = 'xhtml'
    charset = 'utf-8'
    render_style = 'text'

    def get_template(self, meta):
        return loader.select_template([
            f'renderers/html/{meta.app_label}/{meta.model_name}.html',
            f'renderers/html/{meta.app_label}/html.html',
            'renderers/html/html.html'])

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            model = renderer_context['view'].queryset.model
            opts = model._meta
            template = self.get_template(opts)
            if data['results']:
                c = {'data': data,
                     'model': model,
                     'opts': opts,
                     'headers': [labelize(v) for v in data['results'][0].keys()]}
            else:
                c = {'data': {},
                     'model': model,
                     'opts': opts,
                     'headers': []}
            return template.render(c)
        except Exception as e:
            process_exception(e)
            logger.exception(e)
            raise Exception('Error processing request')
