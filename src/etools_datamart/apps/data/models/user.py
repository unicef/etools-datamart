from django.db import models
from month_field.models import MonthField

from etools_datamart.apps.data.models.base import DataMartModel


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
