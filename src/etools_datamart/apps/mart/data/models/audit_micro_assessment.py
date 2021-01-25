from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models import Count
from django.utils.translation import gettext as _

from model_utils import Choices

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.audit_engagement import EngagementMixin
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import AuditEngagement, AuditMicroassessment, AuditRisk

from .partner import Partner


class MicroAssessmentLoader(EngagementMixin, EtoolsLoader):
    def get_subject_area(self, record: AuditEngagement, values: dict, **kwargs):
        value, extra = self._get_risk(record, "ma_subject_areas")
        values["subject_area_extra"] = extra
        return value

    def get_test_subject_areas(self, record: AuditEngagement, values: dict, **kwargs):
        return list(AuditRisk.objects.filter(
            engagement=record,
            blueprint__category__parent__code="ma_subject_areas",
        ).values("blueprint__category__header").annotate(
            count=Count("blueprint__category__header"),
        ).order_by("blueprint__category__header"))

    def process_country(self):
        for record in AuditMicroassessment.objects.select_related('engagement_ptr'):
            record.id = record.engagement_ptr_id
            record.sub_type = AuditMicroassessment
            record.engagement_ptr._impl = record
            filters = self.config.key(self, record.engagement_ptr)
            values = self.get_values(record.engagement_ptr)
            op = self.process_record(filters, values)
            self.increment_counter(op)


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
    subject_area = models.TextField(blank=True, null=True)
    subject_area_extra = JSONField(blank=True, null=True, default=dict)
    test_subject_areas = models.TextField(blank=True, null=True)

    loader = MicroAssessmentLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditMicroassessment
        sync_deleted_records = lambda a: False
        depends = (Partner,)
        mapping = dict(
            agreement="agreement.order_number",  # PurchaseOrder
            partner="-",
            rating="-",
            rating_extra="i",
            subject_area="-",
            subject_area_extra="i",
            test_subject_areas="-",
        )
