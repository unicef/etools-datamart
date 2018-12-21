from functools import wraps

import coreapi
import coreschema
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import connections
from django.http import Http404
from drf_querystringfilter.exceptions import QueryFilterException
from dynamic_serializer.core import InvalidSerializerError
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response

from unicef_rest_framework.ds import DynamicSerializerFilter
from unicef_rest_framework.filtering import SystemFilterBackend
from unicef_rest_framework.ordering import OrderingFilter
from unicef_rest_framework.views import URFReadOnlyModelViewSet
from unicef_rest_framework.views_mixins import IQYConnectionMixin

from etools_datamart.api.filtering import CountryFilter, DatamartQueryStringFilterBackend, TenantCountryFilter
from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.apps.multitenant.exceptions import InvalidSchema, NotAuthorizedSchema

__all__ = ['APIMultiTenantReadOnlyModelViewSet']


class UpdatesMixin:

    @action(methods=['get'], detail=False)
    def updates(self, request, version):
        """ Returns only records changed from last ETL task"""
        task = EtlTask.objects.get_for_model(self.queryset.model)
        if task.last_changes:
            offset = task.last_changes.strftime('%Y-%m-%d %H:%M')
            queryset = self.queryset.filter(last_modify_date__gte=offset)
        else:
            offset = 'none'
            queryset = self.queryset.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,
                        headers={'update-date': offset})


class APIReadOnlyModelViewSet(URFReadOnlyModelViewSet, IQYConnectionMixin):
    filter_backends = [CountryFilter,
                       DatamartQueryStringFilterBackend,
                       OrderingFilter,
                       DynamicSerializerFilter,
                       ]
    # filter_fields = ['country_name']
    ordering_fields = ('id',)
    ordering = 'id'

    def get_schema_fields(self):
        ret = []
        return ret

    def drf_ignore_filter(self, request, field):
        return field in [self.serializer_field_param,
                         self.dynamic_fields_param,
                         'cursor', CountryFilter.query_param, 'month',
                         'ordering', 'page_size', 'format', 'page']

    def handle_exception(self, exc):
        conn = connections['etools']
        if isinstance(exc, (QueryFilterException,)):
            # FieldError can happen due cache attempt to create
            return Response({"error": str(exc)}, status=400)
        elif isinstance(exc, NotAuthenticated):
            return Response({"error": "Authentication credentials were not provided."}, status=401)
        elif isinstance(exc, Http404):
            return Response({"error": "object not found"}, status=404)
        elif isinstance(exc, NotAuthorizedSchema):
            return Response({"error": str(exc)}, status=403)
        elif isinstance(exc, PermissionDenied):
            return Response({"error": str(exc)}, status=403)
        elif isinstance(exc, InvalidSerializerError):
            return Response({"error": str(exc)}, status=400)
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
    filter_backends = [TenantCountryFilter,
                       SystemFilterBackend,
                       DatamartQueryStringFilterBackend,
                       OrderingFilter,
                       DynamicSerializerFilter,
                       ]
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


class DataMartViewSet(APIReadOnlyModelViewSet, UpdatesMixin):
    pass
