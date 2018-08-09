from rest_framework.renderers import JSONRenderer
from unicef_rest_framework.views import ReadOnlyModelViewSet as BaseReadOnlyModelViewSet

from ..renderers import APIBrowsableAPIRenderer

__all__ = ['ReadOnlyModelViewSet']


class ReadOnlyModelViewSet(BaseReadOnlyModelViewSet):
    renderer_classes = [JSONRenderer,
                        APIBrowsableAPIRenderer]
