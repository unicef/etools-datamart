from django.db import models
from month_field.models import MonthField

from etools_datamart.apps.data.models.base import DataMartModel


class FAMIndicator(DataMartModel):
    month = MonthField("Month Value")

    spotcheck_ip_contacted = models.IntegerField(verbose_name='Spot Check-IP Contacted', default=0)
    spotcheck_report_submitted = models.IntegerField(verbose_name='Spot Check-Report Submitted', default=0)
    spotcheck_final_report = models.IntegerField(verbose_name='Spot Check-Final Report', default=0)
    spotcheck_cancelled = models.IntegerField(verbose_name='Spot Check-Cancelled', default=0)
    audit_ip_contacted = models.IntegerField(verbose_name='Audit-IP Contacted', default=0)
    audit_report_submitted = models.IntegerField(verbose_name='Audit-Report Submitted', default=0)
    audit_final_report = models.IntegerField(verbose_name='Audit-Final Report', default=0)
    audit_cancelled = models.IntegerField(verbose_name='Audit-Cancelled', default=0)
    specialaudit_ip_contacted = models.IntegerField(verbose_name='Special Audit-IP Contacted', default=0)
    specialaudit_report_submitted = models.IntegerField(verbose_name='Special Audit-Report Submitted', default=0)
    specialaudit_final_report = models.IntegerField(verbose_name='Special Audit-Final Report', default=0)
    specialaudit_cancelled = models.IntegerField(verbose_name='Special Audit-Cancelled', default=0)
    microassessment_ip_contacted = models.IntegerField(verbose_name='Micro Assessment-IP Contacted', default=0)
    microassessment_report_submitted = models.IntegerField(verbose_name='Micro Assessment-Report Submitted', default=0)
    microassessment_final_report = models.IntegerField(verbose_name='Micro Assessment-Final Report', default=0)
    microassessment_cancelled = models.IntegerField(verbose_name='Micro Assessment-Cancelled', default=0)

    class Meta:
        ordering = ('month', 'country_name')
