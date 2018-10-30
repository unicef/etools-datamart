from datetime import datetime
from functools import lru_cache

import coreapi
import coreschema
from babel._compat import force_text
from django.db import connections, models
from drf_querystringfilter.backend import QueryStringFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import BaseFilterBackend
from unicef_rest_framework.exceptions import InvalidQueryValueError

from etools_datamart.apps.etools.utils import get_etools_allowed_schemas, validate_schemas
from etools_datamart.apps.multitenant.exceptions import NotAuthorizedSchema

SCHEMAMAP = {
    models.BooleanField: coreschema.Boolean,
    models.IntegerField: coreschema.Integer,
    models.DecimalField: coreschema.Number,
    # models.DateField: coreschema.Anything,
}

months = ['jan', 'feb', 'mar',
          'apr', 'may', 'jun',
          'jul', 'aug', 'sep',
          'oct', 'nov', 'dec']


class TenantQueryStringFilterBackend(QueryStringFilterBackend):

    @lru_cache(100)
    def get_schema_fields(self, view):
        ret = []
        for field in view.filter_fields:
            model = view.serializer_class.Meta.model
            model_field = model._meta.get_field(field)
            coreapi_type = SCHEMAMAP.get(type(model_field), coreschema.String)
            ret.append(coreapi.Field(
                name=field,
                required=False,
                location='query',
                schema=coreapi_type(
                    title=force_text(field),
                    description=f'{model_field.help_text} - django queryset syntax allowed'
                )
            ))
        return ret


class MonthFilterBackend(BaseFilterBackend):
    @lru_cache(100)
    def get_schema_fields(self, view):
        model = view.serializer_class.Meta.model
        model_field = model._meta.get_field('month')
        coreapi_type = SCHEMAMAP.get(type(model_field), coreschema.String)
        return [coreapi.Field(
            name='month',
            required=False,
            location='query',
            schema=coreapi_type(
                title=force_text('month'),
                description=r"""selected month. Month can be expressed as:<br/>
                <ul>
<li>[1..12]: month number from jan to dec</li>
<li>[jan..dec]: month short name</li>
<li>[1..12-year]: month number and year if year is different by current year</li>
<li><i>current</i>: <b>current</b> keyword always returns current month</li>
"""
            )
        )]

    def filter_queryset(self, request, queryset, view):
        value = request.GET.get('month', "").lower()
        m = y = None
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
                # elif value == 'latest':
                #     m = datetime.now().month
                #     y = datetime.now().year
                return queryset.filter(month__month=int(m),
                                       month__year=int(y))
            except ValueError:
                raise InvalidQueryValueError('month', value)
        return queryset


class SchemaFilterBackend(BaseFilterBackend):
    @lru_cache(100)
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='country_name',
            required=False,
            location='query',
            schema=coreschema.String(
                title='country_name',
                description="""case insensitive, comma separated list of country names<br/>
{c}
""".format(c=", ".join([c.name for c in connections['etools'].get_tenants()]))
            )
        )]

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


class CountryFilterBackend(SchemaFilterBackend):
    def filter_queryset(self, request, queryset, view):
        value = request.GET.get('country_name', None)
        assert queryset.model._meta.app_label != 'etools'
        if not value:
            if not request.user.is_superuser:
                allowed = get_etools_allowed_schemas(request.user)
                if not allowed:
                    raise PermissionDenied("You don't have enabled schemas")
                queryset.filter(country_name__in=allowed)
        else:
            value = set(value.split(","))
            validate_schemas(*value)
            if not request.user.is_superuser:
                user_schemas = get_etools_allowed_schemas(request.user)
                if not user_schemas.issuperset(value):
                    raise NotAuthorizedSchema(",".join(sorted(value - user_schemas)))
            queryset.filter(country_name__in=value)
        return queryset
