from django.conf import settings
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Count, JSONField
from django.utils.translation import gettext as _

from celery.utils.log import get_task_logger
from model_utils import Choices

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.audit_engagement import EngagementMixin
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts
from etools_datamart.apps.sources.etools.models import AuditEngagement, AuditFinding, AuditSpotcheck

from .partner import Partner

logger = get_task_logger(__name__)


class SpotCheckLoader(EngagementMixin, EtoolsLoader):
    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = AuditSpotcheck.objects.select_related("engagement_ptr").prefetch_related(
            "engagement_ptr__AuditEngagementOffices_engagement"
        )

        paginator = Paginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for record in page.object_list:
                record.id = record.engagement_ptr_id
                record.sub_type = AuditSpotcheck
                record.engagement_ptr._impl = record
                filters = self.config.key(self, record.engagement_ptr)
                values = self.get_values(record.engagement_ptr)
                op = self.process_record(filters, values)
                self.increment_counter(op)

    def _get_priority_findings(self, record: AuditEngagement, priority: str):
        # TODO: Prefetch  related AuditFinding
        return list(
            AuditFinding.objects.filter(
                spot_check=record._impl,
                priority=priority,
            )
            .order_by("category_of_observation")
            .values("category_of_observation")
            .annotate(
                count=Count("category_of_observation"),
            )
        )

    def get_high_priority_findings(self, record: AuditSpotcheck, values: dict, **kwargs):
        return self._get_priority_findings(record, "high")

    def get_low_priority_findings(self, record: AuditSpotcheck, values: dict, **kwargs):
        return self._get_priority_findings(record, "low")

    def get_pending_unsupported_amount(self, record, values, field_name):
        return (
            record._impl.total_amount_of_ineligible_expenditure
            - record.additional_supporting_documentation_provided
            - record.justification_provided_and_accepted
            - record.write_off_required
        )


class SpotCheckFindings(EtoolsDataMartModel):
    TYPE_SPOT_CHECK = "sc"

    TYPES = Choices(
        (TYPE_SPOT_CHECK, _("Spot Check")),
    )
    reference_number = models.CharField(max_length=100, blank=True, null=True)

    engagement_type = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        choices=TYPES,
        db_index=True,
    )
    created = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=30, blank=True, null=True, choices=AuditEngagementConsts.DISPLAY_STATUSES, db_index=True
    )

    # Overview Section
    auditor = models.CharField(max_length=255, blank=True, null=True)
    auditor_number = models.CharField(max_length=30, blank=True, null=True)
    partner = JSONField(blank=True, null=True, default=dict)

    total_value = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    amount_refunded = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    write_off_required = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    pending_unsupported_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    # Overview Card
    spotcheck_total_amount_tested = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20)
    spotcheck_total_amount_of_ineligible_expenditure = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=20
    )
    additional_supporting_documentation_provided = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=20
    )
    justification_provided_and_accepted = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20)
    sections = models.TextField(blank=True, null=True)
    sections_data = JSONField(blank=True, null=True, default=dict)

    # Report Section
    high_priority_findings = JSONField(blank=True, null=True, default=dict)
    low_priority_findings = JSONField(blank=True, null=True, default=dict)

    date_of_field_visit = models.DateField(blank=True, null=True)
    partner_contacted_at = models.DateField(blank=True, null=True)
    date_of_draft_report_to_ip = models.DateField(blank=True, null=True)
    date_of_comments_by_ip = models.DateField(blank=True, null=True)
    date_of_draft_report_to_unicef = models.DateField(blank=True, null=True)
    date_of_comments_by_unicef = models.DateField(blank=True, null=True)
    date_of_report_submit = models.DateField(blank=True, null=True)
    date_of_final_report = models.DateField(null=True, blank=True)
    date_of_cancel = models.DateField(blank=True, null=True)

    offices = models.TextField(blank=True, null=True)
    offices_data = JSONField(blank=True, null=True, default=dict)

    # Action Points
    action_points = JSONField(blank=True, null=True, default=dict)
    action_points_data = JSONField(blank=True, null=True, default=dict)

    loader = SpotCheckLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditSpotcheck
        sync_deleted_records = lambda a: False
        depends = (Partner,)
        mapping = dict(
            auditor="agreement.auditor_firm.organization.name",
            auditor_number="agreement.auditor_firm.organization.vendor_number",
            spotcheck_total_amount_tested="_impl.total_amount_tested",
            spotcheck_total_amount_of_ineligible_expenditure="_impl.total_amount_of_ineligible_expenditure",
            partner="-",
            sections="-",
            pending_unsupported_amount="-",
            high_priority_findings="-",
            low_priority_findings="-",
            action_points="-",
            action_points_data="i",
        )
