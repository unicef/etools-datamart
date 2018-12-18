import sys
from collections import OrderedDict

from django import forms
from django.template import loader
from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class PageFilter(BaseFilterBackend):
    template = 'rest_framework/filters/paging.html'
    pagination_param = 'page_size'

    def get_form(self, request, view):
        Frm = type("SerializerForm", (forms.Form,),
                   {view.pagination_class.page_size_query_param: forms.IntegerField(label="Page Size", required=False)})
        return Frm(request.GET,
                   initial={view.pagination_class.page_size_query_param: self.get_pagination(request, view)})

    def filter_queryset(self, request, queryset, view):
        return queryset

    def get_pagination(self, request, view):
        ps = request.query_params.get(view.pagination_class.page_size_query_param)
        return ps or view.pagination_class.page_size

    def get_template_context(self, request, queryset, view):
        current = self.get_pagination(request, view)
        context = {'request': request,
                   'current': current,
                   'form': self.get_form(request, view),
                   'param': view.pagination_class.page_size_query_param,
                   }
        return context

    def to_html(self, request, queryset, view):
        if view.pagination_class:
            template = loader.get_template(self.template)
            context = self.get_template_context(request, queryset, view)
            return template.render(context)

    def get_default_pagination(self, view):
        return view.pagination_class.page_size


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
    page_size_query_param = 'page_size'

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 10000

    last_page_strings = ('last',)

    def get_paginated_response(self, data):
        if hasattr(self, 'page'):
            return Response(OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('current_page', self.page.number),
                ('total_pages', self.page.paginator.num_pages),
                ('previous', self.get_previous_link()),
                ('results', data)
            ]))
        else:
            return Response(OrderedDict([
                ('count', len(data)),
                ('next', 'N/A'),
                ('current_page', 1),
                ('total_pages', 1),
                ('previous', 'N/A'),
                ('results', data)
            ]))

    def get_page_size(self, request):
        if request._request.GET.get('format') == ['csv', 'iqy', 'xlsx']:
            return sys.maxsize
        try:
            desired = request.query_params[self.page_size_query_param]
            if desired == "-1":
                return sys.maxsize
        except (KeyError, ValueError):
            pass
        return super().get_page_size(request)

    def paginate_queryset(self, queryset, request, view=None):
        # self._handle_backwards_compat(view)
        if self.get_page_size(request) == sys.maxsize:
            return queryset
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
