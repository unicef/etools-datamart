import logging

from crashlog.middleware import process_exception
from drf_renderer_xlsx.renderers import XLSXRenderer as _XLSXRenderer

logger = logging.getLogger(__name__)


class XLSXRenderer(_XLSXRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            if not data['results']:
                return ''
            return super().render(data, accepted_media_type, renderer_context)
        except Exception as e:
            process_exception(e)
            logger.exception(e)
            raise Exception('Error processing request')
