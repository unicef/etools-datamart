from etools_datamart.apps.security.utils import get_allowed_schemas, get_allowed_services  # noqa

# from constance import config
# from django.db import connections
# from unicef_rest_framework.models import Service
# from unicef_security.models import Role
#
# from etools_datamart.apps.etools.models import UsersUserprofile
#
# conn = connections['etools']
#
#
# def get_allowed_schemas(user):
#     if config.DISABLE_SCHEMA_RESTRICTIONS:
#         return sorted(conn.all_schemas)
#
#     if not user.is_authenticated:
#         return []
#     # returns all allowed schemas
#     if user.is_superuser:
#         return conn.all_schemas
#     with conn.noschema():
#         aa = []
#         # aa = list(Role.objects.filter(user=user).values_list('business_area__name', flat=True))
#         etools_user = UsersUserprofile.objects.filter(user__email=user.email).first()
#         if etools_user:
#             aa.extend(set(etools_user.countries_available.values_list('schema_name', flat=True)))
#         else:
#             return conn.all_schemas
#
#     return set(sorted(filter(None, aa)))
#     # return set(map(lambda s: s.lower(), aa))
#
#
# def get_allowed_services(user):
#     if not user.is_authenticated:
#         return []
#     if user.is_superuser or config.DISABLE_SERVICE_RESTRICTIONS:
#         return Service.objects.all()
#     return Service.objects.filter(groupaccesscontrol__group__user=user)
#
# # def schema_is_valid(*schema):
# #     return schema in conn.all_schemas
#
#
# # def validate_schemas(*schemas):
# #     invalid = set(schemas) - conn.all_schemas
# #     if invalid:
# #         raise InvalidSchema(",".join(invalid))
