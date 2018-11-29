from drf_renderer_xlsx.renderers import XLSXRenderer as _XLSXRenderer


class XLSXRenderer(_XLSXRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not data['results']:
            return ''
        return super().render(data, accepted_media_type, renderer_context)
