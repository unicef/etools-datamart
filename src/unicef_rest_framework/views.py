# -*- coding: utf-8 -*-
from functools import lru_cache

from drf_querystringfilter.backend import QueryStringFilterBackend
from dynamic_serializer.core import DynamicSerializerMixin
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.pagination import CursorPagination
from unicef_rest_framework import acl
from unicef_rest_framework.filtering import SystemFilterBackend
from unicef_rest_framework.permissions import URFPermission


def paginator(ordering='-created'):
    return type("TenantPaginator", (CursorPagination,), {'ordering': ordering})


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class ReadOnlyModelViewSet(DynamicSerializerMixin, viewsets.ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    default_access = acl.ACL_ACCESS_LOGIN
    filter_backends = [SystemFilterBackend, QueryStringFilterBackend]
    filter_blacklist = []
    filter_fields = []
    ordering_fields = []
    pagination_class = paginator()
    permission_classes = [URFPermission, ]
    serializers_fieldsets = {}

    @classproperty
    def label(cls):
        return cls.__name__.replace("ViewSet", "")

    @classmethod
    @lru_cache()
    def get_service(cls):
        from unicef_rest_framework.models import Service
        return Service.objects.get_for_viewset(cls)[0]
