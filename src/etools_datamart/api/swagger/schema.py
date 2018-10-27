# # -*- coding: utf-8 -*-
# import logging
#
# import coreschema
# from drf_yasg import openapi
# from drf_yasg.inspectors import SwaggerAutoSchema
# from drf_yasg.utils import force_real_str
#
# logger = logging.getLogger(__name__)
#
#
# class APIAutoSchema(SwaggerAutoSchema):
#     def coreapi_field_to_parameter(self, field):
#         """Convert an instance of `coreapi.Field` to a swagger :class:`.Parameter` object.
#
#         :param coreapi.Field field:
#         :rtype: openapi.Parameter
#         """
#         location_to_in = {
#             'query': openapi.IN_QUERY,
#             'path': openapi.IN_PATH,
#             'form': openapi.IN_FORM,
#             'body': openapi.IN_FORM,
#         }
#         coreapi_types = {
#             coreschema.Integer: openapi.TYPE_INTEGER,
#             coreschema.Number: openapi.TYPE_NUMBER,
#             coreschema.String: openapi.TYPE_STRING,
#             coreschema.Boolean: openapi.TYPE_BOOLEAN,
#         }
#         return openapi.Parameter(
#             name=field.name,
#             in_=location_to_in[field.location],
#             type=coreapi_types.get(type(field.schema), openapi.TYPE_STRING),
#             required=field.required,
#             description=force_real_str(field.schema.description) if field.schema else None,
#         )
#
#     def get_query_parameters(self):
#         ret = super().get_query_parameters()
#         if hasattr(self._sch.view, 'get_schema_fields'):  # pragma: no cover
#             ret += [self.coreapi_field_to_parameter(field) for field in
#                     self._sch.view.get_schema_fields()]
#         return ret
