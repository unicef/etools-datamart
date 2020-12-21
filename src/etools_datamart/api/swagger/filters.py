import logging

from drf_yasg.inspectors import CoreAPICompatInspector

logger = logging.getLogger(__name__)


class APIFilterInspector(CoreAPICompatInspector):
    pass
    # def get_filter_parameters(self, filter_backend):
    #     fields = []
    #     if hasattr(filter_backend, 'get_schema_fields'):
    #         fields = filter_backend.get_schema_fields(self.view)
    #
    #     # if hasattr(self.view, 'get_schema_fields'):
    #     #     fields += self.view.get_schema_fields()
    #     return [self.coreapi_field_to_parameter(field) for field in fields]
