import logging

from crashlog.middleware import process_exception
from rest_framework_csv import renderers as r

logger = logging.getLogger(__name__)


class CSVRenderer(r.CSVRenderer):

    def render(self, data, media_type=None, renderer_context=None, writer_opts=None):
        try:
            data = dict(data)['results']
            return super().render(data, media_type, renderer_context or {}, writer_opts)
        except Exception as e:
            process_exception(e)
            logger.exception(e)
            raise Exception('Error processing request')
