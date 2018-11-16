from rest_framework_csv import renderers as r


class CSVRenderer(r.CSVRenderer):

    def render(self, data, media_type=None, renderer_context=None, writer_opts=None):
        data = dict(data)['results']
        return super().render(data, media_type, renderer_context or {}, writer_opts)
