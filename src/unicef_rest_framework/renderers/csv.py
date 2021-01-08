import logging

from rest_framework_csv import renderers as r

from unicef_rest_framework.renderers.mixin import ContentDispositionMixin

logger = logging.getLogger(__name__)


class CSVRenderer(ContentDispositionMixin, r.CSVRenderer):

    def render(self, data, media_type=None, renderer_context=None, writer_opts=None):
        response = renderer_context['response']
        self.process_response(renderer_context)
        if response.status_code != 200:
            return ''
        try:
            if data and 'results' in data:
                data = dict(data)['results']
            return super().render(data, media_type, renderer_context, writer_opts)
        except Exception as e:
            logger.exception(e)
            raise Exception('Error processing request')
