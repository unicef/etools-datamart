from datetime import datetime

from django.contrib.admin import FieldListFilter
from django.utils.dates import MONTHS

from month_field.models import MonthField

today = datetime.today()


class MonthAdminFilter(FieldListFilter):
    template = 'month_field/admin/filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.param_year_name = field_path + '_year'
        self.param_month_name = field_path + '_month'
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.param_year_name, self.param_month_name]

    def month(self):
        return int(self.used_parameters.get(self.expected_parameters()[1]) or 0)

    def year(self):
        return int(self.used_parameters.get(self.expected_parameters()[0]) or today.year)

    def choices(self, changelist):
        yield {
            'selected': self.month() == 0,
            'this_year': today.year,
            'year': self.year(),
            'value': 0,
            'query_string': changelist.get_query_string({}, ['month', 'year']),
            'label': 'Not set',
            'param_month_name': self.param_month_name,
            'param_year_name': self.param_year_name,

        }
        for num, name in MONTHS.items():
            yield {
                'selected': num == self.month(),
                'this_year': today.year,  # this is tricky...
                'year': self.year(),  # this is tricky...
                'value': num,
                'query_string': changelist.get_query_string({}, ['month', 'year']),
                'label': name,
            }

    def queryset(self, request, queryset):
        if self.month():
            date = datetime(self.year(), self.month(), 1)
            return queryset.filter(month=date)
        return queryset


FieldListFilter.register(lambda f: isinstance(f, MonthField), MonthAdminFilter, True)
