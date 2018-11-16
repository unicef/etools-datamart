# -*- coding: utf-8 -*-
import logging

from drf_querystringfilter.backend import QueryStringFilterBackend
from rest_framework.filters import BaseFilterBackend
from unicef_rest_framework.models import SystemFilter

logger = logging.getLogger(__name__)


class SystemFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filters = {}
        if request.user and request.user.is_authenticated:
            filters['user'] = request.user
        else:
            return queryset

        filters['service'] = view.get_service()

        filter = SystemFilter.objects.match(request, view)
        if filter:
            queryset = filter.filter_queryset(queryset)
            view.store('system-filter', filter.get_querystring())
        return queryset


class CoreAPIQueryStringFilterBackend(QueryStringFilterBackend):
    pass
