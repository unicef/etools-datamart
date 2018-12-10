from datetime import datetime

from django.core.cache import caches
from django.db import connections
from django.db.models import Q
from drf_querystringfilter.exceptions import InvalidQueryValueError
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import BaseFilterBackend
from unicef_rest_framework.filtering import CoreAPIQueryStringFilterBackend

from etools_datamart.apps.etools.models import UsersCountry
from etools_datamart.apps.etools.utils import conn, get_allowed_schemas
from etools_datamart.apps.multitenant.exceptions import InvalidSchema, NotAuthorizedSchema

# from unicef_rest_framework.state import state
cache = caches['api']

months = ['jan', 'feb', 'mar',
          'apr', 'may', 'jun',
          'jul', 'aug', 'sep',
          'oct', 'nov', 'dec']


def get_schema_names(query_args):
    """ accept a string with a comma separated list of names,codes,bussines aread codes
    and returns a set of schema names

    >>> get_schema_names("Bolivia,4020,SYR")
    set('bolivia', 'sudan', 'syria')

    """
    values = sorted(set(query_args.split(",")))
    key = hash(str(values))
    schemas = cache.get(key)
    if not schemas:
        _s = conn.schemas
        conn.set_schemas([])
        schemas = []
        errors = []
        for entry in values:
            try:
                if entry.isdigit():
                    country = UsersCountry.objects.get(business_area_code=entry)
                else:
                    f = Q(name=entry) | Q(schema_name=entry) | Q(country_short_code=entry)
                    country = UsersCountry.objects.get(f)
                schemas.append(country.schema_name)
            # except UsersCountry.MultipleObjectsReturned:
                # this is an issue only during tests
                # country = UsersCountry.objects.filter(f).first()
                # schemas.append(country.schema_name)
            except UsersCountry.DoesNotExist:
                errors.append(entry)
        conn.set_schemas(_s)
        if errors:
            raise InvalidSchema(*errors)
        cache.set(key, schemas)
    return set(filter(None, schemas))


class CountryFilter(BaseFilterBackend):
    query_param = 'country_name'

    # @cached_property
    # def valid_schemas(self):
    #     conn = connections['etools']
    #     return conn.all_schemas

    def get_query(self, request):
        if f"{self.query_param}!" in request.GET:
            return True, request.GET.get(f"{self.query_param}!", "")
        elif self.query_param in request.GET:
            return False, request.GET.get(self.query_param, "")

        return "", ""

    def get_filters(self, request):
        negate, value = self.get_query(request)
        if not value:
            if request.user.is_superuser:
                return []
            else:
                return get_allowed_schemas(request.user)

        if negate:
            exclude = get_schema_names(value)
            selection = get_allowed_schemas(request.user) - exclude
        else:
            selection = get_schema_names(value)
            self.check_permission(request, selection)
        return selection

    def check_permission(self, request, selection):
        if not request.user.is_superuser:
            user_schemas = get_allowed_schemas(request.user)
            if not user_schemas.issuperset(selection):
                raise NotAuthorizedSchema(",".join(sorted(selection - user_schemas)))

    def filter_queryset(self, request, queryset, view):
        selection = self.get_filters(request)
        if not selection:
            if request.user.is_superuser:
                pass
            else:
                raise PermissionDenied("You don't have enabled schemas")
        else:
            queryset = queryset.filter(country_name__in=selection)
        return queryset
        # selection = self.get_filters(request)
        # if selection:
        #     queryset = queryset.filter(country_name__in=selection)
        # view.store(self.__class__.__name__, selection)
        # return queryset


class TenantCountryFilter(CountryFilter):
    def filter_queryset(self, request, queryset, view):
        assert queryset.model._meta.app_label == 'etools'
        conn = connections['etools']
        selection = self.get_filters(request)
        if not selection:
            if request.user.is_superuser:
                conn.set_all_schemas()
            else:
                raise PermissionDenied("You don't have enabled schemas")
        else:
            conn.set_schemas(selection)
        # if not selection:
        #
        #     # FIXME: pdb
        #     import pdb; pdb.set_trace()
        #
        #     if request.user.is_superuser:
        #         conn.set_all_schemas()
        #     else:
        #         allowed = get_allowed_schemas(request.user)
        #         if not allowed:
        #             raise PermissionDenied("You don't have enabled schemas")
        #         conn.set_schemas(allowed)
        # else:
        #     if not request.user.is_superuser:
        #         user_schemas = get_allowed_schemas(request.user)
        #         if not user_schemas.issuperset(selection):
        #             raise NotAuthorizedSchema(",".join(sorted(selection - user_schemas)))
        #     conn.set_schemas(selection)
        # view.store(self.__class__.__name__, conn.schemas)
        return queryset


# class CountryNameProcessor:
#     def ssprocess_country_name(self, efilters, eexclude, field, value, request,
#                                op, param, negate, **payload):
#         filters = {}
#         if value:
#             value = process_country_value(value)
#             if not request.user.is_superuser:
#                 user_schemas = get_etools_allowed_schemas(request.user)
#                 if not user_schemas.issuperset(value):
#                     raise NotAuthorizedSchema(",".join(sorted(value - user_schemas)))
#             filters['country_name__iregex'] = r'(' + '|'.join(value) + ')'
#         else:
#             if not request.user.is_superuser:
#                 allowed = get_etools_allowed_schemas(request.user)
#                 if not allowed:  # pragma: no cover
#                     raise PermissionDenied("You don't have enabled schemas")
#                 filters['country_name__iregex'] = r'(' + '|'.join(allowed) + ')'
#
#         if negate:
#             return {}, filters
#         else:
#             return filters, {}


# class CountryNameProcessorTenantModel(CountryNameProcessor):
#     pass


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
                else:  # pragma: no cover
                    raise InvalidQueryValueError('month', value)

                filters['month__month'] = int(m)
                filters['month__year'] = int(y)
            except ValueError:  # pragma: no cover
                raise InvalidQueryValueError('month', value)
        return filters, exclude


class SetHeaderMixin:
    # must be the first one
    def filter_queryset(self, request, queryset, view):
        ret = super().filter_queryset(request, queryset, view)
        request._filters = self.filters
        request._exclude = self.exclude
        return ret


class DatamartQueryStringFilterBackend(SetHeaderMixin,
                                       CoreAPIQueryStringFilterBackend,
                                       MonthProcessor,
                                       # CountryNameProcessor,
                                       ):
    pass

# class TenantQueryStringFilterBackend(SetHeaderMixin,
#                                      CoreAPIQueryStringFilterBackend,
#                                      MonthProcessor,
#                                      CountryNameProcessorTenantModel,
#                                      ):
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
#             # value = set(value.split(","))
#             # validate_schemas(*value)
#             schemas = process_country_value(value)
#             if not request.user.is_superuser:
#                 user_schemas = get_etools_allowed_schemas(request.user)
#                 if not user_schemas.issuperset(schemas):
#                     raise NotAuthorizedSchema(",".join(sorted(schemas - user_schemas)))
#             conn.set_schemas(schemas)
#         return queryset
