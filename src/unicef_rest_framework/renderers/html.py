from django.template import loader
from rest_framework.renderers import BaseRenderer


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
            'renderers/html/html.html'])

    def render(self, data, accepted_media_type=None, renderer_context=None):
        model = renderer_context['view'].queryset.model
        opts = model._meta
        template = self.get_template(opts)
        c = {'data': data,
             'model': model,
             'opts': opts,
             'headers': [labelize(v) for v in data['results'][0].keys()]}
        return template.render(c)
