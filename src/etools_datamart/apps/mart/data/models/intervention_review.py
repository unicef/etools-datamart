# PartnersInterventionreview
# PartnersPrcofficerinterventionreview
from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Intervention
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention_epd import InterventionSimpleAbstract
from etools_datamart.apps.sources.etools.models import PartnersInterventionreview


class InterventionReviewLoader(EtoolsLoader):
    def get_overall_approver(self, record: PartnersInterventionreview, values: dict, **kwargs):
        if record.overall_approver:
            return "{0.last_name} {0.first_name} ({0.email})".format(record.overall_approver)

    def get_submitted_by(self, record: PartnersInterventionreview, values: dict, **kwargs):
        if record.submitted_by:
            return "{0.last_name} {0.first_name} ({0.email})".format(record.submitted_by)


class InterventionReview(InterventionSimpleAbstract, EtoolsDataMartModel):
    review_created = models.DateTimeField()
    review_modified = models.DateTimeField()
    review_type = models.CharField(max_length=50, blank=True, null=True)
    overall_approval = models.BooleanField(blank=True, null=True)
    # amendment = models.ForeignKey(PartnersInterventionamendment, models.DO_NOTHING, related_name='PartnersInterventionreview_amendment', blank=True, null=True)

    actions_list = models.TextField(blank=True, null=True)
    budget_is_aligned = models.CharField(max_length=100, blank=True, null=True)
    ges_considered = models.CharField(max_length=100, blank=True, null=True)
    meeting_date = models.DateField(blank=True, null=True)
    overall_approver = models.CharField(max_length=2048, blank=True, null=True)
    overall_comment = models.TextField(blank=True, null=True)
    partner_comparative_advantage = models.CharField(max_length=100, blank=True, null=True)
    pd_is_guided = models.CharField(max_length=100, blank=True, null=True)
    pd_is_relevant = models.CharField(max_length=100, blank=True, null=True)
    relationship_is_represented = models.CharField(max_length=10, blank=True, null=True)
    relationships_are_positive = models.CharField(max_length=100, blank=True, null=True)
    supply_issues_considered = models.CharField(max_length=100, blank=True, null=True)
    submitted_by = models.CharField(max_length=2048, blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    sent_back_comment = models.TextField(blank=True, null=True)

    loader = InterventionReviewLoader()

    class Options:
        source = PartnersInterventionreview
        depends = (Intervention,)
        mapping = dict(
            pd_number="intervention.number",
            pd_title="intervention.title",
            partner="intervention.agreement.partner.name",
            partner_cso_type="intervention.agreement.partner.cso_type",
            partner_type="intervention.agreement.partner.partner_type",
            partner_vendor_number="intervention.agreement.partner.vendor_number",
            review_created="created",
            review_modified="modified",
            overall_approver="-",
            submitted_by="-",
        )
        queryset = lambda: PartnersInterventionreview.objects.select_related(
            "intervention", "intervention__agreement", "intervention__agreement__partner"
        )
