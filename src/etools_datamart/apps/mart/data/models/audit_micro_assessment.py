from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models import Count
from django.utils.translation import gettext as _

from model_utils import Choices

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.audit_engagement import EngagementRiskMixin
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import AuditEngagement, AuditFinding, AuditMicroassessment

from .partner import Partner


class MicroAssessmentLoader(EngagementRiskMixin, EtoolsLoader):
    def get_partner(self, record: AuditEngagement, values: dict, **kwargs):
        try:
            p = Partner.objects.get(
                schema_name=self.context['country'].schema_name,
                source_id=record.partner.pk)
            return {
                'name': p.name,
                'vendor_number': p.vendor_number,
                'id': p.pk,
                'source_id': p.source_id,
            }
        except Partner.DoesNotExist:
            return {
                'name': 'N/A',
                'vendor_number': 'N/A',
                'id': 'N/A',
                'source_id': 'N/A',
            }

    def get_test_subject_areas(self, record: AuditEngagement, values: dict, **kwargs):
        value, extra = self._get_risk(record, "ma_subject_areas")
        values["test_subject_areas_extra"] = extra
        return value

    def process_country(self):
        for record in AuditMicroassessment.objects.select_related('engagement_ptr'):
            record.id = record.engagement_ptr_id
            record.sub_type = AuditMicroassessment
            record.engagement_ptr._impl = record
            filters = self.config.key(self, record.engagement_ptr)
            values = self.get_values(record.engagement_ptr)


class MicroAssessment(EtoolsDataMartModel):
    TYPE_MICRO_ASSESSMENT = 'ma'

    TYPES = Choices(
        (TYPE_MICRO_ASSESSMENT, _('Micro Assessment')),
    )

    engagement_type = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        choices=TYPES,
        db_index=True,
    )
    agreement = models.CharField(max_length=300, blank=True, null=True)
    partner = JSONField(blank=True, null=True, default=dict)
    date_of_field_visit = models.DateField(null=True, blank=True)
    date_of_final_report = models.DateField(null=True, blank=True)
    shared_ip_with = ArrayField(
        models.CharField(max_length=20, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        verbose_name=_('Shared Audit with'),
    )
    rating = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    rating_extra = JSONField(blank=True, null=True, default=dict)
    test_subject_areas = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    test_subject_areas_extra = JSONField(blank=True, null=True, default=dict)

    loader = MicroAssessmentLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditMicroassessment
        sync_deleted_records = lambda a: False
        depends = (Partner,)
        mapping = dict(
            agreement="agreement.order_number",
            partner="-",
            rating="-",
            rating_extra="i",
            test_subject_areas="-",
            test_subject_areas_extra="i",
        )
