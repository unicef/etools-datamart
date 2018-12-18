# -*- coding: utf-8 -*-
from functools import lru_cache

import rest_framework_extensions.utils
from drf_querystringfilter.backend import QueryStringFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from strategy_field.utils import fqn
from unicef_rest_framework.pagination import PageFilter

from . import acl
from .auth import AnonymousAuthentication, IPBasedAuthentication, JWTAuthentication, URLTokenAuthentication
from .cache import cache_response, etag, ListKeyConstructor
from .ds import DynamicSerializerFilter, DynamicSerializerMixin
from .filtering import SystemFilterBackend
from .negotiation import CT
from .ordering import OrderingFilter
from .permissions import ServicePermission
from .renderers import (HTMLRenderer, IQYRenderer, MSJSONRenderer, MSXmlRenderer,
                        PDFRenderer, TextRenderer, URFBrowsableAPIRenderer, XLSXRenderer,)
from .renderers.csv import CSVRenderer


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class URFReadOnlyModelViewSet(DynamicSerializerMixin, viewsets.ReadOnlyModelViewSet):
    serializer_field_param = '-serializer'
    dynamic_fields_param = '+fields'

    object_cache_key_func = rest_framework_extensions.utils.default_object_cache_key_func
    list_cache_key_func = ListKeyConstructor()

    object_etag_func = rest_framework_extensions.utils.default_object_etag_func
    list_etag_func = ListKeyConstructor()

    authentication_classes = (SessionAuthentication,
                              IPBasedAuthentication,
                              JWTAuthentication,
                              BasicAuthentication,
                              TokenAuthentication,
                              IPBasedAuthentication,
                              URLTokenAuthentication,
                              AnonymousAuthentication,
                              )
    default_access = acl.ACL_ACCESS_LOGIN
    content_negotiation_class = CT
    filter_backends = [QueryStringFilterBackend,
                       OrderingFilter,
                       DynamicSerializerFilter]

    renderer_classes = [JSONRenderer,
                        URFBrowsableAPIRenderer,
                        CSVRenderer,
                        YAMLRenderer,
                        XLSXRenderer,
                        HTMLRenderer,
                        PDFRenderer,
                        MSJSONRenderer,
                        XMLRenderer,
                        MSXmlRenderer,
                        TextRenderer,
                        IQYRenderer,
                        ]
    ordering_fields = ('id',)
    ordering = 'id'
    filter_blacklist = []
    filter_fields = []
    # pagination_class = paginator()
    permission_classes = [ServicePermission, ]
    serializers_fieldsets = {}

    def get_filter_backends(self, removes=None):
        flt = list(self.filter_backends)
        if SystemFilterBackend not in flt:
            flt.insert(0, SystemFilterBackend)
        if PageFilter not in flt:
            flt.append(PageFilter)
        return list(filter(removes, flt))

    def filter_queryset(self, queryset):
        for backend in self.get_filter_backends():
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def store(self, key, value):
        self.request._request.api_info[key] = value

    def dispatch(self, request, *args, **kwargs):
        request._view = self
        if hasattr(request, 'api_info'):
            request.api_info["view"] = fqn(self)
            request.api_info["service"] = self.get_service()

        return super().dispatch(request, *args, **kwargs)

    # def filter_queryset(self, queryset):
    #     if hasattr(self.request, 'api_info'):
    #         self.request.api_info["sql"] = str(queryset.query)
    #     return super().filter_queryset(queryset)

    @classproperty
    def label(cls):
        return cls.__name__.replace("ViewSet", "")

    @classmethod
    @lru_cache()
    def get_service(cls):
        from unicef_rest_framework.models import Service
        return Service.objects.get_for_viewset(cls)

    # @classproperty
    # def endpoint(self):
    #     for __, viewset, base_name in conf.ROUTER.registry:
    #         if viewset == self:
    #             return reverse(f'api:{base_name}-list', args=['latest'])
    #     return None

    @etag(etag_func='object_etag_func')
    @cache_response(key_func='object_cache_key_func', cache='api')
    def retrieve(self, request, *args, **kwargs):
        return super(URFReadOnlyModelViewSet, self).retrieve(request, *args, **kwargs)

    @etag(etag_func='list_etag_func')
    @cache_response(key_func='list_cache_key_func', cache='api')
    def list(self, request, *args, **kwargs):
        return super(URFReadOnlyModelViewSet, self).list(request, *args, **kwargs)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if hasattr(self.request.accepted_renderer, 'disable_pagination'):
            return None
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()

        return self._paginator

    def paginate_queryset(self, queryset):
        return super().paginate_queryset(queryset)

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)
