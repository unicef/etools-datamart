from django.template import loader

from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework.pagination import _positive_int

from unicef_rest_framework.ds import DynamicSerializerFilter
from unicef_rest_framework.pagination import APIPagination

from etools_datamart.api.endpoints.common import BaseAPIReadOnlyModelViewSet
from etools_datamart.api.filtering import DatamartQueryStringFilterBackend
from etools_datamart.apps.mart.rapidpro.models import Organization


class RapidProPagination(APIPagination):
    page_size = 10
    max_page_size = 1000

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size


class OrganizationFilter(BaseFilterBackend):
    query_param = 'organization'
    template = 'api/select2_filter.html'

    def get_query(self, request):
        if f"{self.query_param}!" in request.GET:
            return True, ",".join(request.GET.getlist(f"{self.query_param}!", ""))
        elif self.query_param in request.GET:
            return False, ",".join(request.GET.getlist(self.query_param, ""))
        return "", ""

    def get_query_args(self, request):
        self.query_args = []
        negate, value = self.get_query(request)
        if value:
            self.query_args = [int(a) for a in value.split(',')]
        self.negate = negate

    def filter_queryset(self, request, queryset, view):
        self.get_query_args(request)
        if self.query_args:
            queryset = queryset.filter(organization__id__in=self.query_args)
        return queryset

    def to_html(self, request, queryset, view):
        self.get_query_args(request)
        template = loader.get_template(self.template)
        context = {'elements': Organization.objects.values_list('id', 'name'),
                   'selection': self.query_args,
                   'query_param': self.query_param,
                   'label': 'Organization',
                   'header': 'aaaaaa'}
        return template.render(context, request)


class RapidProViewSet(BaseAPIReadOnlyModelViewSet):
    pagination_class = RapidProPagination
    filter_backends = [OrganizationFilter,
                       DatamartQueryStringFilterBackend,
                       OrderingFilter,
                       DynamicSerializerFilter,
                       ]

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()

        return self._paginator
