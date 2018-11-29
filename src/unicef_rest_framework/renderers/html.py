from django.template import loader
from rest_framework.renderers import BaseRenderer


class HTMLRenderer(BaseRenderer):
    media_type = 'text/html'
    format = 'xhtml'
    charset = 'utf-8'
    render_style = 'text'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        model = renderer_context['view'].queryset.model
        opts = model._meta
        template = loader.select_template([
            f'renderers/{opts.app_label}/{opts.model_name}.html',
            'renderers/html.html'])
        c = {'data': data,
             'model': model,
             'opts': opts,
             'headers': data['results'][0].keys()}
        return template.render(c)
