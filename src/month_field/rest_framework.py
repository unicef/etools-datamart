from datetime import date, datetime
from functools import lru_cache

import coreapi
import coreschema
from coreapi.compat import force_text
from django.forms import forms
from django.template import loader
from django.utils.dates import MONTHS_3
from drf_querystringfilter.exceptions import InvalidQueryValueError
from month_field.forms import MonthField
from rest_framework.filters import BaseFilterBackend


class MonthForm(forms.Form):
    month = MonthField()


def clean(value):
    months = list(MONTHS_3.values())
    if '-' in value:
        m, y = value.split('-')
        y = y or datetime.now().year
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
    else:
        m = 0
        y = 0
    return int(m), int(y)


class MonthFilterBackend(BaseFilterBackend):
    template = 'month_field/rest_framework/month_filtering.html'
    month_param = 'month'

    def get_value(self, request):
        raw_value = request.query_params.get(self.month_param, "")
        return clean(raw_value)

    def get_form(self, request, view, context):
        month, year = context['current']
        Frm = type("MonthForm", (forms.Form,),
                   {self.month_param: MonthField(label="Month",
                                                 required=False)})
        if month:
            return Frm(initial={self.month_param: date(day=1, month=month, year=year)})
        else:
            return Frm()

    def get_template_context(self, request, queryset, view):
        current = self.get_value(request)
        context = {
            'request': request,
            'current': current,
        }
        context['form'] = self.get_form(request, view, context)
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

        if value:
            try:
                m, y = clean(value)
                return queryset.filter(month__month=int(m),
                                       month__year=int(y))
            except ValueError:
                raise InvalidQueryValueError('month', value)
        return queryset
