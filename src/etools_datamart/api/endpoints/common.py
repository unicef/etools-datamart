from functools import wraps
from inspect import isclass

from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import connections
from django.http import Http404

import coreapi
import coreschema
from drf_querystringfilter.exceptions import QueryFilterException
from dynamic_serializer.core import DynamicSerializer, InvalidSerializerError
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from sentry_sdk import capture_exception
from strategy_field.utils import fqn

from unicef_rest_framework.ds import DynamicSerializerFilter
from unicef_rest_framework.filtering import SystemFilterBackend
from unicef_rest_framework.ordering import OrderingFilter
from unicef_rest_framework.views import URFReadOnlyModelViewSet
from unicef_rest_framework.views_mixins import IQYConnectionMixin

from etools_datamart.api.filtering import CountryFilter, DatamartQueryStringFilterBackend, TenantCountryFilter
from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.apps.multitenant.exceptions import InvalidSchema, NotAuthorizedSchema
from etools_datamart.libs.mystica import MysticaBasicAuthentication

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


class AutoRegisterMetaClass(type):
    registry = {}

    def __new__(mcs, class_name, bases, attrs):
        new_class = super().__new__(mcs, class_name, bases, attrs)
        mcs.registry[fqn(new_class)] = new_class
        return new_class


class APIReadOnlyModelViewSet(URFReadOnlyModelViewSet, IQYConnectionMixin,
                              metaclass=AutoRegisterMetaClass):
    filter_backends = [CountryFilter,
                       DatamartQueryStringFilterBackend,
                       OrderingFilter,
                       DynamicSerializerFilter,
                       ]
    authentication_classes = URFReadOnlyModelViewSet.authentication_classes + (MysticaBasicAuthentication,)
    ordering_fields = ('id',)
    ordering = 'id'
    family = 'datamart'

    def get_schema_fields(self):
        ret = []
        return ret

    def drf_ignore_filter(self, request, field):
        return field in [self.serializer_field_param,
                         self.dynamic_fields_param,
                         'cursor', CountryFilter.query_param, 'month',
                         'ordering', 'page_size', 'format', 'page']

    def raise_uncaught_exception(self, exc):
        capture_exception(exc)
        return super().raise_uncaught_exception(exc)

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
            except (TypeError, ValueError, ValidationError, ObjectDoesNotExist):  # pragma: no cover
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
    family = 'etools'
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
    querystringfilter_form_base_class = forms.Form

    def _get_serializer_from_param(self, name=None):
        if name is None:
            name = self.request.query_params.get(self.serializer_field_param, 'std')

        if name == 'std':
            return self._default_serializer

        target = self.serializers_fieldsets.get(name, None)
        if isinstance(target, DynamicSerializer):
            field_list = target.get_fields(self)
            return self._build_serializer_from_fields(field_list)
        elif isinstance(target, (list, tuple)):
            return self._build_serializer_from_fields(target)
        elif isclass(target):  # Serializer class
            return target
        else:  # Standard Serializer
            raise InvalidSerializerError

    def get_querystringfilter_form(self, request, filter):
        return self.querystringfilter_form_base_class(request.GET, filter.form_prefix)
