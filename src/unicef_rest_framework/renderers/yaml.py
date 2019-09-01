import logging

from crashlog.middleware import process_exception
from rest_framework_yaml.renderers import YAMLRenderer as BaseRenderer

from unicef_rest_framework.renderers.mixin import ContentDispositionMixin

logger = logging.getLogger(__name__)


def labelize(v):
    return v.replace("_", " ").title()


class YAMLRenderer(ContentDispositionMixin, BaseRenderer):
    format = 'yaml'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']
        self.process_response(renderer_context)
        if response.status_code != 200:
            return ''
        try:
            return super().render(data, accepted_media_type, renderer_context)

        except Exception as e:
            process_exception(e)
            logger.exception(e)
            raise Exception(f'Error processing request {e}') from e
