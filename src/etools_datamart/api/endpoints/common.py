from functools import wraps, lru_cache

import coreapi
import coreschema
from babel._compat import force_text
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.http import Http404
from drf_querystringfilter.backend import QueryStringFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_csv import renderers as r
from unicef_rest_framework.views import ReadOnlyModelViewSet as BaseReadOnlyModelViewSet

from etools_datamart.state import state

from ..renderers import APIBrowsableAPIRenderer

__all__ = ['MultiTenantReadOnlyModelViewSet']

SCHEMAMAP = {
    models.BooleanField: coreschema.Boolean,
    models.IntegerField: coreschema.Integer,
    models.DecimalField: coreschema.Number,
    # models.DateField: coreschema.Anything,
}


class TenantQueryStringFilterBackend(QueryStringFilterBackend):

    @lru_cache(100)
    def get_schema_fields(self, view):
        ret = []
        if hasattr(view, 'filter_fields'):
            for field in view.filter_fields:
                model = view.serializer_class.Meta.model
                model_field = model._meta.get_field(field)
                coreapi_type = SCHEMAMAP.get(type(model_field), coreschema.String)
                ret.append(coreapi.Field(
                    name=field,
                    required=False,
                    location='query',
                    schema=coreapi_type(
                        title=force_text(field),
                        description=f'{model_field.help_text} - django queryset synthax allowed'
                    )
                ))
        return ret

    @property
    def query_params(self):
        """
        More semantically correct name for request.GET.
        """
        params = self.request._request.GET
        if 'country_name' in params:
            state.schemas = []
        return params


class ReadOnlyModelViewSet(BaseReadOnlyModelViewSet):
    renderer_classes = [JSONRenderer,
                        APIBrowsableAPIRenderer,
                        r.CSVRenderer,
                        ]
    filter_backends = [TenantQueryStringFilterBackend]

    def drf_ignore_filter(self, request, field):
        return field in '_schemas'

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        selection = self.kwargs[lookup_url_kwarg]
        if selection == '_lastest_':
            queryset = self.filter_queryset(self.get_queryset())
            try:
                obj = queryset.latest('id')
            except (TypeError, ValueError, ValidationError, ObjectDoesNotExist):
                raise Http404
            else:
                self.check_object_permissions(self.request, obj)
                return obj

        return super().get_object()


def set_schema_header(func):
    @wraps(func)
    def _inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        ret['X-Schema'] = ','.join(state.schemas)
        return ret

    return _inner


class MultiTenantReadOnlyModelViewSet(ReadOnlyModelViewSet):
    @set_schema_header
    def retrieve(self, request, *args, **kwargs):
        if not state.schemas:
            return Response({'error': 'Please set X-Schema header with selected workspace'}, status=400)
        if len(state.schemas) > 1:
            return Response({'error': 'Please set X-Schema header with only one workspace'}, status=400)
        return super().retrieve(request, *args, **kwargs)

    @set_schema_header
    def list(self, request, *args, **kwargs):
        if not state.schemas:
            return Response({'error': 'Please set X-Schema header with selected workspaces'}, status=400)
        return super().list(request, *args, **kwargs)
