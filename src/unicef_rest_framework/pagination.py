from collections import OrderedDict

from rest_framework import serializers
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class CurrentPageField(serializers.Field):
    page_field = 'page'

    def to_native(self, value):
        page = value.number
        return page


class NumPagesField(serializers.Field):
    page_field = 'page'

    def to_native(self, value):
        pages = value.paginator.num_pages
        return pages


class APIPagination(PageNumberPagination):
    page_size = 100
    page_query_param = 'page'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = None

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 1000

    last_page_strings = ('last',)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('current_page', self.page.number),
            ('total_pages', self.page.paginator.num_pages),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_page_size(self, request):
        if request._request.GET.get('format') == 'csv':
            return 999999999
        return super().get_page_size(request)

    def paginate_queryset(self, queryset, request, view=None):
        # self._handle_backwards_compat(view)
        return super(APIPagination, self).paginate_queryset(queryset, request, view)

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)


def paginator(ordering='-created'):
    return type("TenantPaginator", (CursorPagination,), {'ordering': ordering})


CreationPaginator = paginator()
