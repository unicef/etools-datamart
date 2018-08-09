# -*- coding: utf-8 -*-
from drf_querystringfilter.backend import QueryStringFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import CursorPagination


class ApiMixin:
    permission_classes = []


def paginator(ordering='-created'):
    return type("TenantPaginator", (CursorPagination,), {'ordering': ordering})


class ReadOnlyModelViewSet(ApiMixin, viewsets.ReadOnlyModelViewSet):
    pagination_class = paginator()
    filter_backends = [QueryStringFilterBackend]
    filter_blacklist = []
    filter_fields = []
