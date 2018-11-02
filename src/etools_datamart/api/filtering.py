from datetime import datetime

from django.db import connections
from drf_querystringfilter.exceptions import InvalidQueryArgumentError, InvalidQueryValueError
from rest_framework.exceptions import PermissionDenied
from unicef_rest_framework.filtering import CoreAPIQueryStringFilterBackend

from etools_datamart.apps.etools.utils import get_etools_allowed_schemas, validate_schemas
from etools_datamart.apps.multitenant.exceptions import NotAuthorizedSchema
from etools_datamart.state import state

months = ['jan', 'feb', 'mar',
          'apr', 'may', 'jun',
          'jul', 'aug', 'sep',
          'oct', 'nov', 'dec']


# class SchemaFilterBackend(BaseFilterBackend):
#     @lru_cache(100)
#     def get_schema_fields(self, view):
#         return [coreapi.Field(
#             name='country_name',
#             required=False,
#             location='query',
#             schema=coreschema.String(
#                 title='country_name',
#                 description="""case insensitive, comma separated list of country names<br/>
# {c}
# """.format(c=", ".join([c.name for c in connections['etools'].get_tenants()]))
#             )
#         )]
#
#     def filter_queryset(self, request, queryset, view):
#         value = request.GET.get('country_name', None)
#         assert queryset.model._meta.app_label == 'etools'
#         conn = connections['etools']
#         if not value:
#             if request.user.is_superuser:
#                 conn.set_all_schemas()
#             else:
#                 allowed = get_etools_allowed_schemas(request.user)
#                 if not allowed:
#                     raise PermissionDenied("You don't have enabled schemas")
#                 conn.set_schemas(get_etools_allowed_schemas(request.user))
#         else:
#             value = set(value.split(","))
#             validate_schemas(*value)
#             if not request.user.is_superuser:
#                 user_schemas = get_etools_allowed_schemas(request.user)
#                 if not user_schemas.issuperset(value):
#                     raise NotAuthorizedSchema(",".join(sorted(value - user_schemas)))
#             conn.set_schemas(value)
#         return queryset
# class CountryFilterBackend(SchemaFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         value = request.GET.get('country_name', None)
#         assert queryset.model._meta.app_label != 'etools'
#         if not value:
#             if not request.user.is_superuser:
#                 allowed = get_etools_allowed_schemas(request.user)
#                 if not allowed:
#                     raise PermissionDenied("You don't have enabled schemas")
#                 queryset.filter(country_name__in=allowed)
#         else:
#             value = set(value.split(","))
#             validate_schemas(*value)
#             if not request.user.is_superuser:
#                 user_schemas = get_etools_allowed_schemas(request.user)
#                 if not user_schemas.issuperset(value):
#                     raise NotAuthorizedSchema(",".join(sorted(value - user_schemas)))
#             queryset.filter(country_name__in=value)
#         return queryset


class CountryNameProcessor:
    def process_country_name(self, efilters, eexclude, field, value, request,
                             op, param, negate, **payload):
        if op:
            raise InvalidQueryArgumentError(param)
        filters = {}
        if not value:
            if not request.user.is_superuser:
                allowed = get_etools_allowed_schemas(request.user)
                if not allowed:
                    raise PermissionDenied("You don't have enabled schemas")
                filters['country_name__iregex'] = r'(' + '|'.join(allowed) + ')'
        else:
            value = set(value.lower().split(","))
            validate_schemas(*value)
            if not request.user.is_superuser:
                user_schemas = get_etools_allowed_schemas(request.user)
                if not user_schemas.issuperset(value):
                    raise NotAuthorizedSchema(",".join(sorted(value - user_schemas)))
            filters['country_name__iregex'] = r'(' + '|'.join(value) + ')'

        if negate:
            return {}, filters
        else:
            return filters, {}


class CountryNameProcessorTenantModel(CountryNameProcessor):

    def process_country_name(self, filters, exclude, field, value, request, **payload):
        _f, _e = super().process_country_name({}, {}, field, value, request, **payload)
        # assert queryset.model._meta.app_label == 'etools'
        conn = connections['etools']
        if 'country_name__iregex' in _f:
            conn.set_schemas(_f['country_name__iregex'])
        else:
            conn.set_all_schemas()

        return filters, exclude


class MonthProcessor:
    def process_month(self, filters, exclude, field, value, **payload):
        if value:
            try:
                if '-' in value:
                    m, y = value.split('-')
                else:
                    m = value
                    y = datetime.now().year

                if m in months:
                    m = months.index(m) + 1
                elif m in list(map(str, range(12))):
                    m = m
                elif value == 'current':
                    m = datetime.now().month
                    y = datetime.now().year

                filters['month__month'] = int(m)
                filters['month__year'] = int(y)
            except ValueError:
                raise InvalidQueryValueError('month', value)
        return filters, exclude


class SetHeaderMixin:
    # must be the first one
    def filter_queryset(self, request, queryset, view):
        ret = super().filter_queryset(request, queryset, view)
        state.set('filters', self.filters)
        state.set('excludes', self.exclude)
        return ret


class DatamartQueryStringFilterBackend(SetHeaderMixin,
                                       CoreAPIQueryStringFilterBackend,
                                       MonthProcessor,
                                       CountryNameProcessor,
                                       ):
    pass


class TenantQueryStringFilterBackend(SetHeaderMixin,
                                     CoreAPIQueryStringFilterBackend,
                                     MonthProcessor,
                                     CountryNameProcessorTenantModel,
                                     ):
    def filter_queryset(self, request, queryset, view):
        value = request.GET.get('country_name', None)
        assert queryset.model._meta.app_label == 'etools'
        conn = connections['etools']
        if not value:
            if request.user.is_superuser:
                conn.set_all_schemas()
            else:
                allowed = get_etools_allowed_schemas(request.user)
                if not allowed:
                    raise PermissionDenied("You don't have enabled schemas")
                conn.set_schemas(get_etools_allowed_schemas(request.user))
        else:
            value = set(value.split(","))
            validate_schemas(*value)
            if not request.user.is_superuser:
                user_schemas = get_etools_allowed_schemas(request.user)
                if not user_schemas.issuperset(value):
                    raise NotAuthorizedSchema(",".join(sorted(value - user_schemas)))
            conn.set_schemas(value)
        return queryset
