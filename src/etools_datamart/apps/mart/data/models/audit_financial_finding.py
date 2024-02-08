from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Audit
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts, AuditFinancialFindingsConsts
from etools_datamart.apps.sources.etools.models import AuditFinancialfinding


class AuditFinancialfindingLoader(EtoolsLoader):
    def process_country(self):
        country = self.context["country"]
        for record in self.filter_queryset(self.get_queryset()):
            try:
                audit = Audit.objects.get(source_id=record.audit_id, schema_name=country.schema_name)
                filters = self.config.key(self, record)
                values = self.get_values(record)
                values["partner_vendor_number"] = audit.auditor_number
                values["partner_name"] = audit.auditor
                values["audit_reference_number"] = audit.reference_number
                values["audit_status"] = audit.status
                op = self.process_record(filters, values)
                self.increment_counter(op)
            except Audit.DoesNotExist:
                pass


class AuditFinancialFinding(EtoolsDataMartModel):
    created = models.DateField(auto_now=True)

    partner_vendor_number = models.CharField(max_length=50, blank=True, null=True)
    partner_name = models.CharField(max_length=255, blank=True, null=True)

    audit_reference_number = models.CharField(max_length=100, blank=True, null=True)
    audit_status = models.CharField(
        max_length=30, blank=True, null=True, choices=AuditEngagementConsts.DISPLAY_STATUSES, db_index=True
    )

    title = models.CharField(max_length=255, choices=AuditFinancialFindingsConsts.TITLE_CHOICES)
    local_amount = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    recommendation = models.TextField(blank=True)
    ip_comments = models.TextField(blank=True)

    loader = AuditFinancialfindingLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditFinancialfinding
        depends = (Audit,)
        key = lambda loader, record: dict(
            schema_name=loader.context["country"].schema_name,
            source_id=record.id,
        )
