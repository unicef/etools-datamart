from django.core.cache import caches
from django.db import connections
from django.db.models import Q
from django.template import loader
from django.utils.functional import cached_property

from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import BaseFilterBackend

from unicef_rest_framework.filtering import CoreAPIQueryStringFilterBackend

from etools_datamart.apps.etools.models import UsersCountry
from etools_datamart.apps.multitenant.exceptions import InvalidSchema, NotAuthorizedSchema
from etools_datamart.apps.security.utils import conn, get_allowed_schemas

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
    template = 'api/country_filter.html'

    # @cached_property
    # def valid_schemas(self):
    #     conn = connections['etools']
    #     return conn.all_schemas

    def get_query(self, request):
        if f"{self.query_param}!" in request.GET:
            return True, ",".join(request.GET.getlist(f"{self.query_param}!", ""))
        elif self.query_param in request.GET:
            return False, ",".join(request.GET.getlist(self.query_param, ""))

        return "", ""

    def get_query_args(self, request):
        negate, value = self.get_query(request)
        if not value:
            if request.user.is_superuser:
                self.query_args = []
            else:
                self.query_args = get_allowed_schemas(request.user)
        else:
            self.query_args = get_schema_names(value)
        self.negate = negate

    def get_filters(self, request):
        self.get_query_args(request)
        if self.negate:
            exclude = self.query_args
            selection = get_allowed_schemas(request.user) - exclude
        else:
            selection = self.query_args
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
            queryset = queryset.filter(schema_name__in=selection)
        return queryset

    def to_html(self, request, queryset, view):
        self.get_query_args(request)
        template = loader.get_template(self.template)
        context = {'countries': sorted(conn.all_schemas),
                   'selection': self.query_args,
                   'header': 'aaaaaa'}
        return template.render(context, request)


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
        return queryset


#

class SetHeaderMixin:
    # must be the first one
    def filter_queryset(self, request, queryset, view):
        ret = super().filter_queryset(request, queryset, view)
        request._filters = self.filters
        request._exclude = self.exclude
        return ret


class DatamartQueryStringFilterBackend(SetHeaderMixin,
                                       CoreAPIQueryStringFilterBackend,
                                       # MonthProcessor,
                                       # CountryNameProcessor,
                                       ):
    pass


class CountryNameFilter(BaseFilterBackend):
    query_param = 'country_name'
    template = 'api/country_filter.html'

    def get_query(self, request):
        if f"{self.query_param}!" in request.GET:
            return True, ",".join(request.GET.getlist(f"{self.query_param}!", ""))
        elif self.query_param in request.GET:
            return False, ",".join(request.GET.getlist(self.query_param, ""))

        return "", ""

    @cached_property
    def all_countries(self):
        return sorted(UsersCountry.objects.values_list('name', flat=True))

    def get_query_args(self, request):
        negate, value = self.get_query(request)
        if not value:
            if request.user.is_superuser:
                self.query_args = []
            else:
                self.query_args = self.all_countries
        else:
            self.query_args = value.split(',')
        self.negate = negate

    def filter_queryset(self, request, queryset, view):
        self.get_query_args(request)
        if self.query_args:
            if self.negate:
                queryset = queryset.exclude(country_name__in=self.query_args)
            else:
                queryset = queryset.filter(country_name__in=self.query_args)
        return queryset

    def to_html(self, request, queryset, view):
        self.get_query_args(request)
        template = loader.get_template(self.template)
        context = {'countries': self.all_countries,
                   'selection': self.query_args,
                   'header': 'aaaaaa'}
        return template.render(context, request)
