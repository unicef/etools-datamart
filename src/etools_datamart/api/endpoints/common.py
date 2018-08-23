from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from etools_datamart.state import state
from unicef_rest_framework.views import ReadOnlyModelViewSet as BaseReadOnlyModelViewSet

from ..renderers import APIBrowsableAPIRenderer

__all__ = ['ReadOnlyModelViewSet']


class ReadOnlyModelViewSet(BaseReadOnlyModelViewSet):
    renderer_classes = [JSONRenderer,
                        APIBrowsableAPIRenderer]

    def retrieve(self, request, *args, **kwargs):
        if not state.schemas:
            return Response({'error': 'Please set X-Schema header with selected workspace'}, status=400)
        if len(state.schemas) > 1:
            return Response({'error': 'Please set X-Schema header with only one workspace'}, status=400)
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not state.schemas:
            return Response({'error': 'Please set X-Schema header with selected workspaces'}, status=400)
        return super().list(request, *args, **kwargs)

