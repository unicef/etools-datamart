# -*- coding: utf-8 -*-
import logging

from rest_framework.filters import BaseFilterBackend
from unicef_rest_framework.models import SystemFilter

logger = logging.getLogger(__name__)


class SystemFilterBackend(BaseFilterBackend):
    def get_filters_for(self, target):
        """
            returns filters for target

        :param target: User

        :return:
        """
        return SystemFilter.objects.filter(user=target)

    def filter_queryset(self, request, queryset, view):
        filters = {}
        if request.user and request.user.is_authenticated:
            filters['user'] = request.user
        else:
            return queryset

        filters['service'] = view.get_service()

        filter = SystemFilter.objects.filter(**filters).first()
        if filter:
            queryset = filter.filter_queryset(queryset)
            request._request._system_filter = filter.get_querystring()
        return queryset
