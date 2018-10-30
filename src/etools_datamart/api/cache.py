from django.core.cache import caches
from django.utils.http import quote_etag
from rest_framework_extensions.cache.decorators import CacheResponse
from rest_framework_extensions.etag.decorators import ETAGProcessor
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.bits import KeyBitBase
from rest_framework_extensions.key_constructor.constructors import KeyConstructor
from rest_framework_extensions.settings import extensions_api_settings
from unicef_rest_framework.cache import parse_ttl

from etools_datamart.state import state


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
    headers = bits.HeadersKeyBit(['Accept'])
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
        request._request.service = view_instance.get_service()
        request._request.viewset = view_instance
        # state.set('service', view_instance.get_service().name)
        # state.set('viewset', fqn(view_instance))
        state.set('cache-ttl', view_instance.get_service().cache_ttl)

        if not hasattr(response, '_closable_objects'):  # pragma: no cover
            response._closable_objects = []

        return response


etag = APIETAGProcessor
cache_response = APICacheResponse
