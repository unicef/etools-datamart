from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext as _

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Partner
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import PseaAnswer, PseaAssessment, PseaAssessmentFocalPoints


class PseaAssessmentLoader(EtoolsLoader):

    def get_assessor(self, record: PseaAssessment, values: dict, **kwargs):
        assessor = getattr(record, 'PseaAssessor_assessment', None)
        if assessor:
            return {
                'assessor_type': assessor.assessor_type,
                'name': assessor.auditor_firm.name if assessor.auditor_firm else assessor.user.email
            }

    def get_focal_points(self, record: PseaAssessment, values: dict, **kwargs):
        focal_points = record.PseaAssessmentFocalPoints_assessment.all()
        if focal_points:
            return [fp.user.email for fp in focal_points]


class PseaAssessment(EtoolsDataMartModel):
    partner_name = models.CharField(blank=True, null=True, max_length=255)
    cso_type = models.CharField(max_length=50, blank=True, null=True)
    vendor_number = models.CharField(max_length=30, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    overall_rating = models.IntegerField(blank=True, null=True)
    assessment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    assessor = models.JSONField(blank=True, null=True, default=dict)
    focal_points = models.JSONField(blank=True, null=True, default=dict)

    loader = PseaAssessmentLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = PseaAssessment
        depends = (Partner, )
        mapping = dict(
            partner_name="partner.name",
            vendor_number="partner.vendor_number",
            cso_type="partner.cso_type",
            assessor='-',
            focal_points='-'
        )


class PseaAnswer(EtoolsDataMartModel):
    assessment_partner_name = models.CharField(blank=True, null=True, max_length=255)
    assessment_cso_type = models.CharField(max_length=50, blank=True, null=True)
    assessment_vendor_number = models.CharField(max_length=30, blank=True, null=True)
    assessment_reference_number = models.CharField(max_length=100, blank=True, null=True)
    assessment_status = models.CharField(max_length=30, blank=True, null=True)
    assessment_date = models.DateField(blank=True, null=True)

    indicator_subject = models.TextField(null=True, blank=True)
    indicator_content = models.TextField(null=True, blank=True)
    indicator_active = models.BooleanField(null=True, blank=True)
    indicator_rating_instructions = models.TextField(null=True, blank=True)

    rating_label = models.CharField(max_length=50, null=True, blank=True)
    rating_active = models.BooleanField(null=True, blank=True)

    comments = models.TextField(blank=True, null=True)

    loader = EtoolsLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = PseaAnswer
        depends = (Partner, PseaAssessment)
        mapping = dict(
            assessment_partner_name="assessment.partner.name",
            assessment_cso_type="assessment.partner.cso_type",
            assessment_vendor_number="assessment.partner.vendor_number",
            assessment_reference_number="assessment.reference_number",
            assessment_status="assessment.status",
            assessment_date="assessment.assessment_date",
            indicator_subject="indicator.subject",
            indicator_content="indicator.content",
            indicator_active = "indicator.active",
            indicator_rating_instructions="indicator.rating_instructions",
            rating_label="rating.label",
            rating_active="rating.active"

        )


