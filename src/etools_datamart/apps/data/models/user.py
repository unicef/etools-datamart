from datetime import datetime

from django.db import models

from month_field.models import MonthField

from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import AuthUser


class UserStatsLoader(Loader):
    def get_context(self, **kwargs):
        today = kwargs['today']
        context = {'first_of_month': datetime(today.year, today.month, 1)}
        context.update(kwargs)
        return context

    def process_country(self, country, context):
        first_of_month = context['first_of_month']
        base = AuthUser.objects.filter(profile__country=country)
        values = {
            'total': base.count(),
            'unicef': base.filter(email__endswith='@unicef.org').count(),
            'logins': base.filter(
                last_login__month=first_of_month.month).count(),
            'unicef_logins': base.filter(
                last_login__month=first_of_month.month,
                email__endswith='@unicef.org').count(),
        }
        op = self.process(filters=dict(month=first_of_month,
                                       country_name=country.name,
                                       schema_name=country.schema_name, ),
                          values=values)
        self.results.incr(op)


class UserStats(DataMartModel):
    month = MonthField("Month Value")
    total = models.IntegerField("Total users", default=0)
    unicef = models.IntegerField("UNICEF uswers", default=0)
    logins = models.IntegerField("Number of logins", default=0)
    unicef_logins = models.IntegerField("Number of UNICEF logins", default=0)

    class Meta:
        ordering = ('-month', 'country_name')
        unique_together = ('country_name', 'month')
        verbose_name = "User Access Statistics"

    loader = UserStatsLoader()
