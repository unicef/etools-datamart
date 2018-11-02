from django.contrib.admin import ListFilter


class MonthAdminFilter(ListFilter):
    template = 'month_field/admin/filter.html'
