from django.db import models
from django.utils.translation import gettext as _

from model_utils import Choices
from month_field import Month
from month_field.models import MonthField

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import (
    AuditAudit,
    AuditEngagement,
    AuditMicroassessment,
    AuditSpecialaudit,
    AuditSpotcheck,
)


class FAMIndicatorLoader(EtoolsLoader):
    PARTNER_CONTACTED = "partner_contacted"
    REPORT_SUBMITTED = "report_submitted"
    FINAL = "final"
    CANCELLED = "cancelled"

    STATUSES = Choices(
        (PARTNER_CONTACTED, _("IP Contacted")),
        (REPORT_SUBMITTED, _("Report Submitted")),
        (FINAL, _("Final Report")),
        (CANCELLED, _("Cancelled")),
    )

    def get_values(self, record):
        pass  # pragma: no cover

    def process_country(self):
        country = self.context["country"]
        start_date = self.context["today"].date()
        month = Month.from_date(start_date)
        FAMIndicator.objects.filter(month=month.as_date(), schema_name=country.schema_name)
        engagements = (AuditSpotcheck, AuditAudit, AuditSpecialaudit, AuditMicroassessment)
        for model in engagements:
            realname = "_".join(model._meta.db_table.split("_")[1:])
            values = self.get_mart_values(country)
            # prepare all fields
            for status, status_display in self.STATUSES:
                filter_dict = {
                    "engagement_ptr__status": status,
                    "engagement_ptr__start_date__month": start_date.month,
                    "engagement_ptr__start_date__year": start_date.year,
                }
                field_name = f"{realname}_{status_display}".replace(" ", "_").lower()
                value = model.objects.filter(**filter_dict).count()
                values[field_name] = value
            op = self.process_record(filters=dict(month=month, country_name=country.name), values=values)
            self.increment_counter(op)


class FAMIndicator(EtoolsDataMartModel):
    month = MonthField("Month Value")

    spotcheck_ip_contacted = models.IntegerField(verbose_name="Spot Check-IP Contacted", default=0)
    spotcheck_report_submitted = models.IntegerField(verbose_name="Spot Check-Report Submitted", default=0)
    spotcheck_final_report = models.IntegerField(verbose_name="Spot Check-Final Report", default=0)
    spotcheck_cancelled = models.IntegerField(verbose_name="Spot Check-Cancelled", default=0)

    audit_ip_contacted = models.IntegerField(verbose_name="Audit-IP Contacted", default=0)
    audit_report_submitted = models.IntegerField(verbose_name="Audit-Report Submitted", default=0)
    audit_final_report = models.IntegerField(verbose_name="Audit-Final Report", default=0)
    audit_cancelled = models.IntegerField(verbose_name="Audit-Cancelled", default=0)

    specialaudit_ip_contacted = models.IntegerField(verbose_name="Special Audit-IP Contacted", default=0)
    specialaudit_report_submitted = models.IntegerField(verbose_name="Special Audit-Report Submitted", default=0)
    specialaudit_final_report = models.IntegerField(verbose_name="Special Audit-Final Report", default=0)
    specialaudit_cancelled = models.IntegerField(verbose_name="Special Audit-Cancelled", default=0)

    microassessment_ip_contacted = models.IntegerField(verbose_name="Micro Assessment-IP Contacted", default=0)
    microassessment_report_submitted = models.IntegerField(verbose_name="Micro Assessment-Report Submitted", default=0)
    microassessment_final_report = models.IntegerField(verbose_name="Micro Assessment-Final Report", default=0)
    microassessment_cancelled = models.IntegerField(verbose_name="Micro Assessment-Cancelled", default=0)

    class Meta:
        ordering = ("month", "country_name")
        unique_together = ("month", "country_name")
        verbose_name = "FAM Indicator"

    loader = FAMIndicatorLoader()

    class Options:
        source = AuditEngagement
        sync_deleted_records = lambda loader: False
        # mapping = dict(source_id='engagement_ptr_id')
