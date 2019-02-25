import logging

from rest_framework_csv import renderers as r

logger = logging.getLogger(__name__)


class JSONRenderer(r.JSONRenderer):
    pass
    # def render(self, data, accepted_media_type=None, renderer_context=None):
    #     response = renderer_context['response']
    #     if response.status_code != 200:
    #         return bytes(''.encode('utf-8'))
    #     try:
    #         if data and 'results' in data:
    #             data = dict(data)['results']
    #         return super().render(data, accepted_media_type, renderer_context)
    #     except Exception as e:
    #         process_exception(e)
    #         logger.exception(e)
    #         raise Exception('Error processing request')
