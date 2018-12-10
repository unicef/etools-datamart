from datetime import datetime

from django.core.cache import caches
from django.db import connections
from django.db.models import Q
from drf_querystringfilter.exceptions import InvalidQueryValueError
from rest_framework.exceptions import PermissionDenied
from unicef_rest_framework.filtering import CoreAPIQueryStringFilterBackend

from etools_datamart.apps.etools.models import UsersCountry
from etools_datamart.apps.etools.utils import conn, get_etools_allowed_schemas
from etools_datamart.apps.multitenant.exceptions import InvalidSchema, NotAuthorizedSchema

# from unicef_rest_framework.state import state
cache = caches['api']

months = ['jan', 'feb', 'mar',
          'apr', 'may', 'jun',
          'jul', 'aug', 'sep',
          'oct', 'nov', 'dec']


def process_country_value(query_args):
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
            #
            except UsersCountry.DoesNotExist:
                errors.append(entry)
        conn.set_schemas(_s)
        if errors:
            raise InvalidSchema(*errors)
        cache.set(key, schemas)
    # else:
    #     schemas = json.loads(schemas)
    # schemas = UsersCountry.objects.filter(Q(name__in=values) |
    #                                       Q(schema_name__in=values) |
    #                                       Q(country_short_code__in=values) |
    #                                       Q(business_area_code__in=values)
    #                                       ).values_list('schema_name', flat=True)
    # if len(schemas) != len(values):
    #     raise InvalidSchema(",".join(values))
    # validate_schemas(*schemas)
    return set(schemas)


class CountryNameProcessor:
    def process_country_name(self, efilters, eexclude, field, value, request,
                             op, param, negate, **payload):
        filters = {}
        if value:
            value = process_country_value(value)
            if not request.user.is_superuser:
                user_schemas = get_etools_allowed_schemas(request.user)
                if not user_schemas.issuperset(value):
                    raise NotAuthorizedSchema(",".join(sorted(value - user_schemas)))
            filters['country_name__iregex'] = r'(' + '|'.join(value) + ')'
        else:
            if not request.user.is_superuser:
                allowed = get_etools_allowed_schemas(request.user)
                if not allowed:  # pragma: no cover
                    raise PermissionDenied("You don't have enabled schemas")
                filters['country_name__iregex'] = r'(' + '|'.join(allowed) + ')'

        if negate:
            return {}, filters
        else:
            return filters, {}


class CountryNameProcessorTenantModel(CountryNameProcessor):
    pass


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
        # state.set('filters', self.filters)
        # state.set('excludes', self.exclude)
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
            # value = set(value.split(","))
            # validate_schemas(*value)
            schemas = process_country_value(value)
            if not request.user.is_superuser:
                user_schemas = get_etools_allowed_schemas(request.user)
                if not user_schemas.issuperset(schemas):
                    raise NotAuthorizedSchema(",".join(sorted(schemas - user_schemas)))
            conn.set_schemas(schemas)
        return queryset
