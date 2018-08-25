# -*- coding: utf-8 -*-
from drf_querystringfilter.backend import QueryStringFilterBackend
from dynamic_serializer.core import DynamicSerializerMixin
from rest_framework import permissions, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.pagination import CursorPagination
from unicef_rest_framework import acl


def paginator(ordering='-created'):
    return type("TenantPaginator", (CursorPagination,), {'ordering': ordering})


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class ApiMixin:
    permission_classes = [permissions.IsAuthenticated]
    default_access = acl.ACL_ACCESS_LOGIN
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    @classproperty
    def label(cls):
        return cls.__name__.replace("ViewSet", "")


class DynamicSerializerViewSet(ApiMixin, DynamicSerializerMixin, viewsets.ModelViewSet):
    pass


class ReadOnlyModelViewSet(ApiMixin, DynamicSerializerMixin, viewsets.ReadOnlyModelViewSet):
    pagination_class = paginator()
    serializers_fieldsets = {}
    filter_backends = [QueryStringFilterBackend]
    filter_blacklist = []
    filter_fields = []
    ordering_fields = []
