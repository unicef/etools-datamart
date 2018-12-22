from django.db import models

from month_field.models import MonthField

from etools_datamart.apps.data.loader import EtlResult, Loader
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import (AuditAudit, AuditEngagement, AuditMicroassessment,
                                                AuditSpecialaudit, AuditSpotcheck,)


class FAMIndicatorLoader(Loader):

    def process_country(self, results: EtlResult, country, context):
        engagements = (AuditSpotcheck, AuditAudit, AuditSpecialaudit, AuditMicroassessment)
        start_date = context['today'].date()
        for model in engagements:
            realname = "_".join(model._meta.db_table.split('_')[1:])
            values = {}
            for status, status_display in AuditEngagement.STATUSES:
                filter_dict = {
                    'engagement_ptr__status': status,
                    'engagement_ptr__start_date__month': start_date.month,
                    'engagement_ptr__start_date__year': start_date.year,
                }
                field_name = f"{realname}_{status_display}".replace(" ", "_").lower()
                value = model.objects.filter(**filter_dict).count()
                values[field_name] = value
            op = self.process(filters=dict(month=start_date,
                                           country_name=country.name,
                                           area_code=country.business_area_code,
                                           schema_name=country.schema_name),
                              values=values)
            results.incr(op)

        return results


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
        unique_together = ('month', 'country_name')
        verbose_name = "FAM Indicator"

    loader = FAMIndicatorLoader()
