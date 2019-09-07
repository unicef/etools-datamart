from rest_framework.pagination import _positive_int

from unicef_rest_framework.pagination import APIPagination

from etools_datamart.api.endpoints.common import BaseAPIReadOnlyModelViewSet


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


class RapidProViewSet(BaseAPIReadOnlyModelViewSet):
    pagination_class = RapidProPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()

        return self._paginator
