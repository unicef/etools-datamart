from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models import Count
from django.utils.translation import gettext as _

from model_utils import Choices

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.audit_engagement import EngagementRiskMixin
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import AuditEngagement, AuditFinancialfinding, AuditSpecialaudit

from .partner import Partner


class AuditSpecialLoader(EngagementRiskMixin, EtoolsLoader):
    def process_country(self):
        for record in AuditSpecialaudit.objects.select_related('engagement_ptr'):
            record.id = record.engagement_ptr_id
            record.sub_type = AuditSpecialaudit
            record.engagement_ptr._impl = record
            filters = self.config.key(self, record.engagement_ptr)
            values = self.get_values(record.engagement_ptr)


class AuditSpecial(EtoolsDataMartModel):
    TYPE_SPECIAL_AUDIT = 'sa'

    TYPES = Choices(
        (TYPE_SPECIAL_AUDIT, _('Special Audit')),
    )

    engagement_type = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        choices=TYPES,
        db_index=True,
    )
    agreement = models.CharField(max_length=300, blank=True, null=True)
    auditor = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    shared_ip_with = ArrayField(
        models.CharField(max_length=20, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        verbose_name=_('Shared Audit with'),
    )
    total_value = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=20,
    )
    date_of_final_report = models.DateField(null=True, blank=True)
    joint_audit = models.BooleanField(null=True, blank=True)
    date_of_field_visit = models.DateField(null=True, blank=True)
    date_of_draft_report_to_ip = models.DateField(null=True, blank=True)
    date_of_comments_by_ip = models.DateField(null=True, blank=True)
    date_of_draft_report_to_unicef = models.DateField(null=True, blank=True)

    loader = AuditSpecialLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditSpecialaudit
        sync_deleted_records = lambda a: False
        depends = (Partner,)
        mapping = dict(
            auditor="agreement.auditor_firm.name",
            partner="-",
        )
