# -*- coding: utf-8 -*-
from functools import lru_cache

from drf_querystringfilter.backend import QueryStringFilterBackend
from dynamic_serializer.core import DynamicSerializerMixin
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.pagination import CursorPagination
from unicef_rest_framework import acl
from unicef_rest_framework.config import conf
from unicef_rest_framework.filtering import SystemFilterBackend
from unicef_rest_framework.permissions import URFPermission


def paginator(ordering='-created'):
    return type("TenantPaginator", (CursorPagination,), {'ordering': ordering})


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class ApiMixin:
    permission_classes = [URFPermission, ]
    default_access = acl.ACL_ACCESS_LOGIN
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    @classproperty
    def label(cls):
        return cls.__name__.replace("ViewSet", "")

    @lru_cache()
    def get_service(self):
        from unicef_rest_framework.models import Service
        try:
            return Service.objects.get(viewset=self)
        except Service.DoesNotExist:
            name = getattr(self, 'label', self.__class__.__name__)
            return Service.objects.create(name=name,
                                          viewset=self,
                                          access=getattr(self, 'default_access',
                                                         conf.DEFAULT_ACCESS),
                                          description=getattr(self, '__doc__', ""))


class DynamicSerializerViewSet(ApiMixin, DynamicSerializerMixin, viewsets.ModelViewSet):
    def get_serializer_class(self, target=None):
        return self.strategy._get_serializer_from_param()


class ReadOnlyModelViewSet(ApiMixin, DynamicSerializerMixin, viewsets.ReadOnlyModelViewSet):
    pagination_class = paginator()
    serializers_fieldsets = {}
    filter_backends = [SystemFilterBackend, QueryStringFilterBackend]
    filter_blacklist = []
    filter_fields = []
    ordering_fields = []
