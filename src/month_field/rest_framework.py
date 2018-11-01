from datetime import datetime
from functools import lru_cache

import coreapi
import coreschema
from coreapi.compat import force_text
from django.forms import forms
from django.template import loader
from django.utils.dates import MONTHS_3
from month_field.forms import MonthField
from rest_framework.filters import BaseFilterBackend
from unicef_rest_framework.exceptions import InvalidQueryValueError


class MonthForm(forms.Form):
    month = MonthField()


class MonthFilterBackend(BaseFilterBackend):
    template = 'month_field/rest_framework/month_filtering.html'
    month_param = 'month'

    def get_value(self, request, queryset, view):
        return request.query_params.get(self.month_param)

    def get_template_context(self, request, queryset, view):
        current = self.get_value(request, queryset, view)
        context = {
            'request': request,
            'form': MonthForm(initial={'month': current}),
        }
        return context

    def to_html(self, request, queryset, view):
        template = loader.get_template(self.template)
        context = self.get_template_context(request, queryset, view)
        return template.render(context)

    @lru_cache(100)
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='month',
            required=False,
            location='query',
            schema=coreschema.String(
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
        months = MONTHS_3.values()
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
