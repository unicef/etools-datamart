import logging

import django_filters
from drf_querystringfilter.backend import QueryStringFilterBackend
from rest_framework.filters import BaseFilterBackend

from unicef_rest_framework.models import Export, SystemFilter

logger = logging.getLogger(__name__)


class SystemFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # _system_filters has been set by cache.SystemFilterKeyBit
        # if hasattr(request._request, "_system_filters"):
        #     if request._request._system_filters:
        #         queryset = request._request._system_filters.filter_queryset(queryset)
        # else:
        filter = SystemFilter.objects.match(request, view)
        if filter:
            queryset = filter.filter_queryset(queryset)
            view.store("system-filters", filter.get_querystring())
        return queryset


class CoreAPIQueryStringFilterBackend(QueryStringFilterBackend):
    pass


class ExportFilter(django_filters.FilterSet):
    filename = django_filters.CharFilter(lookup_expr="icontains", label="Filename")
    name = django_filters.CharFilter(lookup_expr="icontains", label="Description")
    as_user__username = django_filters.CharFilter(lookup_expr="icontains", label="Owner")

    class Meta:
        model = Export
        fields = ["name", "filename", "as_user__username", "format", "refresh", "enabled"]
