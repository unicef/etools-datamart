from functools import wraps

import coreapi
import coreschema
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import connections
from django.http import Http404
from drf_querystringfilter.exceptions import QueryFilterException
from dynamic_serializer.core import DynamicSerializerMixin
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from unicef_rest_framework.filtering import SystemFilterBackend
from unicef_rest_framework.views import ReadOnlyModelViewSet

from etools_datamart.api.filtering import DatamartQueryStringFilterBackend, TenantQueryStringFilterBackend
from etools_datamart.apps.multitenant.exceptions import InvalidSchema, NotAuthorizedSchema

__all__ = ['APIMultiTenantReadOnlyModelViewSet']


class SchemaSerializerField(coreschema.Enum):

    def __init__(self, view: DynamicSerializerMixin, **kwargs):
        self.view = view
        kwargs.setdefault('title', 'serializers')
        kwargs.setdefault('description', self.build_description())
        super().__init__(list(view.serializers_fieldsets.keys()), **kwargs)

    def build_description(self):
        defs = []
        names = []
        for k, v in self.view.serializers_fieldsets.items():
            names.append(k)
            defs.append(f"""- **{k}**: {self.view.get_serializer_fields(k)}
""")

        description = f"""Define the set of fields to return. Allowed values are:
            [{'*, *'.join(names)}*]

{''.join(defs)}
        """
        return description


class APIReadOnlyModelViewSet(ReadOnlyModelViewSet):
    filter_backends = [SystemFilterBackend,
                       DatamartQueryStringFilterBackend,
                       OrderingFilter]
    filter_fields = ['country_name']
    ordering_fields = ('id',)
    ordering = 'id'

    def get_schema_fields(self):
        ret = []
        if self.serializers_fieldsets:
            ret.append(coreapi.Field(
                name=self.serializer_field_param,
                required=False,
                location='query',
                schema=SchemaSerializerField(self)
            ))
        return ret

    def drf_ignore_filter(self, request, field):
        return field in ['+serializer', 'cursor', '+fields',
                         'ordering', 'page_size', 'format', ]

    def handle_exception(self, exc):
        conn = connections['etools']
        if isinstance(exc, QueryFilterException):
            return Response({"error": str(exc)}, status=400)
        elif isinstance(exc, NotAuthenticated):
            return Response({"error": "Authentication credentials were not provided."}, status=401)
        elif isinstance(exc, Http404):
            return Response({"error": "object not found"}, status=404)
        elif isinstance(exc, NotAuthorizedSchema):
            return Response({"error": str(exc)}, status=403)
        elif isinstance(exc, PermissionDenied):
            return Response({"error": str(exc)}, status=403)
        elif isinstance(exc, InvalidSchema):
            return Response({"error": str(exc),
                             "hint": "Removes wrong schema from selection",
                             "valid": sorted(conn.all_schemas)
                             }, status=400)
        return super().handle_exception(exc)

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


def one_schema(func):
    @wraps(func)
    def _inner(self, request, *args, **kwargs):
        if 'country_name' not in request.GET:
            return Response({'error': 'country_name parameter is mandatory'}, status=400)
        if ',' in request.GET['country_name']:
            return Response({'error': 'only one country is allowed'}, status=400)
        ret = func(self, request, *args, **kwargs)
        ret['X-Schema'] = ','.join(connections['etools'].schemas)
        return ret

    return _inner


def schema_header(func):
    @wraps(func)
    def _inner(self, request, *args, **kwargs):
        ret = func(self, request, *args, **kwargs)
        ret['X-Schema'] = ','.join(connections['etools'].schemas)
        return ret

    return _inner


class APIMultiTenantReadOnlyModelViewSet(APIReadOnlyModelViewSet):
    filter_backends = [SystemFilterBackend,
                       TenantQueryStringFilterBackend,
                       OrderingFilter]
    ordering_fields = ('id',)
    ordering = 'id'

    @one_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @schema_header
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_schema_fields(self):
        ret = super(APIMultiTenantReadOnlyModelViewSet, self).get_schema_fields()
        ret.append(coreapi.Field(
            name='_schema',
            required=False,
            location='query',
            schema=coreschema.String(description="comma separated list of schemas")
        ))
        return ret
