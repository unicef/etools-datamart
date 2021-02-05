from django.contrib.admin import ChoicesFieldListFilter, SimpleListFilter

from unicef_rest_framework.utils import humanize_size

KILO = 1024
MEGA = KILO * 1024
GIGA = MEGA * 1024

MS = 1
SECOND = MS * 1000
MINUTE = SECOND * 60


class RangeFilter(SimpleListFilter):
    def lookups(self, request, model_admin):
        return [(a, b[0]) for a, b in self.ranges.items()]

    def value(self):
        return self.used_parameters.get(self.parameter_name)

    def queryset(self, request, queryset):
        if self.value():
            flt = self.ranges[int(self.value())][1]
            if isinstance(flt, dict):
                return queryset.filter(**flt)
            else:
                return queryset.filter(*flt)
        return queryset


class SizeFilter(RangeFilter):
    title = 'Size'
    parameter_name = 'size'
    template = 'adminfilters/combobox.html'

    def __init__(self, request, params, model, model_admin):
        self.ranges = {}
        for i, s in enumerate([KILO,
                               KILO * 10,
                               MEGA,
                               MEGA * 5,
                               MEGA * 10,
                               ]):
            self.ranges[i] = ('> %s' % humanize_size(s), dict(response_length__gt=s))
        super().__init__(request, params, model, model_admin)


class TimeFilter(RangeFilter):
    title = 'Time'
    parameter_name = 'time'
    template = 'adminfilters/combobox.html'

    def __init__(self, request, params, model, model_admin):
        self.ranges = {
            0: ('< 1s', dict(response_ms__lte=SECOND)),
        }
        for sec in range(1, 11):
            self.ranges[sec] = ('> %ss' % sec, dict(response_ms__gte=SECOND * sec))
        super().__init__(request, params, model, model_admin)


class StatusFilter(ChoicesFieldListFilter):
    title = 'Status'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_until = '%s__lt' % field_path

    def choices(self, changelist):
        choices = []
        for item in ['2xx', '3xx', '4xx', '5xx']:
            flt = int(item[0]) * 100
            filterdict = {self.lookup_kwarg_since: flt, self.lookup_kwarg_until: flt + 100}
            choices.append({
                'selected': True,
                'query_string': changelist.get_query_string(filterdict, [self.lookup_kwarg_isnull]),
                'display': item
            },)
        return choices
