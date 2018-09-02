from functools import lru_cache, wraps

import coreapi
import coreschema
import rest_framework_extensions.utils
from babel._compat import force_text
from django.core.cache import caches
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.http import Http404
from django.utils.http import quote_etag
from drf_querystringfilter.backend import QueryStringFilterBackend
from dynamic_serializer.core import DynamicSerializerMixin
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_csv import renderers as r
from rest_framework_extensions.cache.decorators import CacheResponse
from rest_framework_extensions.etag.decorators import ETAGProcessor
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.bits import KeyBitBase
from rest_framework_extensions.key_constructor.constructors import KeyConstructor
from rest_framework_extensions.settings import extensions_api_settings
from unicef_rest_framework.cache import parse_ttl
from unicef_rest_framework.filtering import SystemFilterBackend
from unicef_rest_framework.views import ReadOnlyModelViewSet

from etools_datamart.state import state

from ..renderers import APIBrowsableAPIRenderer

__all__ = ['APIMultiTenantReadOnlyModelViewSet']

SCHEMAMAP = {
    models.BooleanField: coreschema.Boolean,
    models.IntegerField: coreschema.Integer,
    models.DecimalField: coreschema.Number,
    # models.DateField: coreschema.Anything,
}


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


# class TenantQueryStringFilterBackend(QueryStringFilterBackend):

class TenantQueryStringFilterBackend(QueryStringFilterBackend):

    @lru_cache(100)
    def get_schema_fields(self, view):
        ret = []
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


#
# class SystemFilterKeyBit(KeyBitBase):
#     def get_data(self, params, view_instance, view_method, request, args, kwargs):
#         version = view_instance.get_service().cache_version
#         state.set('cache-version', version)
#         return {'system-filter': SystemFilter.objects.match(request, view_instance)}


class CacheVersionKeyBit(KeyBitBase):
    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        version = view_instance.get_service().cache_version
        state.set('cache-version', version)
        return {'cache_version': str(version)}


class ListKeyConstructor(KeyConstructor):
    cache_version = CacheVersionKeyBit()
    # system_filter = SystemFilterKeyBit()

    unique_method_id = bits.UniqueMethodIdKeyBit()
    format = bits.FormatKeyBit()
    headers = bits.HeadersKeyBit(['Accept', 'X-Schema'])
    # language = bits.LanguageKeyBit()
    list_sql_query = bits.ListSqlQueryKeyBit()
    querystring = bits.QueryParamsKeyBit()
    pagination = bits.PaginationKeyBit()

    def get_key(self, view_instance, view_method, request, args, kwargs):
        key = super().get_key(view_instance, view_method, request, args, kwargs)
        state.set('cache-key', key)
        return key


class APIETAGProcessor(ETAGProcessor):
    def is_if_none_match_failed(self, res_etag, etags, if_none_match):
        if res_etag and if_none_match:
            return quote_etag(res_etag) in etags or '*' in etags
        else:
            return False


class APICacheResponse(CacheResponse):
    def __init__(self,
                 timeout=None,
                 key_func=None,
                 cache=None,
                 cache_errors=None):
        self.cache_name = cache or extensions_api_settings.DEFAULT_USE_CACHE
        super(APICacheResponse, self).__init__(timeout=timeout, key_func=key_func,
                                               cache=cache, cache_errors=cache_errors)

    # @staticmethod
    # def get_cache(name):
    #     from django.core.cache import caches
    #     return caches[name]

    def process_cache_response(self,
                               view_instance,
                               view_method,
                               request,
                               args,
                               kwargs):
        key = self.calculate_key(
            view_instance=view_instance,
            view_method=view_method,
            request=request,
            args=args,
            kwargs=kwargs
        )
        cache = caches[self.cache_name]
        response = cache.get(key)
        if not response:
            state.set('cache-hit', False)
            response = view_method(view_instance, request, *args, **kwargs)
            response = view_instance.finalize_response(request, response, *args, **kwargs)
            response.render()  # should be rendered, before picklining while storing to cache

            if not response.status_code >= 400 or self.cache_errors:  # pragma: no cover
                cache.set(key, response, parse_ttl(view_instance.get_service().cache_ttl or '1y'))
        else:
            state.set('cache-hit', True)
        state.set('cache-ttl', view_instance.get_service().cache_ttl)

        if not hasattr(response, '_closable_objects'):  # pragma: no cover
            response._closable_objects = []

        return response


etag = APIETAGProcessor
cache_response = APICacheResponse


class APIReadOnlyModelViewSet(ReadOnlyModelViewSet):
    object_cache_key_func = rest_framework_extensions.utils.default_object_cache_key_func
    list_cache_key_func = ListKeyConstructor()

    object_etag_func = rest_framework_extensions.utils.default_object_etag_func
    list_etag_func = ListKeyConstructor()

    renderer_classes = [JSONRenderer,
                        APIBrowsableAPIRenderer,
                        r.CSVRenderer,
                        ]
    filter_backends = [SystemFilterBackend, TenantQueryStringFilterBackend]
    # schema = DefaultSchema()

    # def filter_queryset(self, queryset):
    #     if not hasattr(self, '_filtered_queryset'):
    #         self._filtered_queryset = super().filter_queryset(queryset)
    #     return self._filtered_queryset

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
        return field in ['_schemas', 'serializer', 'cursor']

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

    @etag(etag_func='object_etag_func')
    @cache_response(key_func='object_cache_key_func', cache='api')
    def retrieve(self, request, *args, **kwargs):
        return super(APIReadOnlyModelViewSet, self).retrieve(request, *args, **kwargs)

    @etag(etag_func='list_etag_func')
    @cache_response(key_func='list_cache_key_func', cache='api')
    def list(self, request, *args, **kwargs):
        return super(APIReadOnlyModelViewSet, self).list(request, *args, **kwargs)


def set_schema_header(func):
    @wraps(func)
    def _inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        ret['X-Schema'] = ','.join(state.schemas)
        return ret

    return _inner


class APIMultiTenantReadOnlyModelViewSet(APIReadOnlyModelViewSet):
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

    def get_schema_fields(self):
        ret = super(APIMultiTenantReadOnlyModelViewSet, self).get_schema_fields()
        ret.append(coreapi.Field(
            name='_schema',
            required=False,
            location='query',
            schema=coreschema.String(description="comma separated list of schemas")
        ))
        return ret
