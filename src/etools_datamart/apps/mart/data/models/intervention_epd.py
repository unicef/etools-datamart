import logging

from django.db import models

from etools_datamart.apps.sources.etools.models import PartnersIntervention

from ..loader import EtoolsLoader
from .base import EtoolsDataMartModel
from .intervention import Intervention, InterventionLoader

logger = logging.getLogger(__name__)


class InterventionSimpleAbstract(models.Model):
    pd_number = models.CharField(max_length=64, blank=True, null=True)
    pd_title = models.CharField(max_length=306, null=True, db_index=True)

    # PARTNER
    partner = models.CharField(max_length=255, blank=True, null=True)
    partner_cso_type = models.CharField(max_length=300, blank=True, null=True)
    partner_type = models.CharField(max_length=50, blank=True, null=True)
    partner_vendor_number = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        abstract = True

    class Options:
        depends = (Intervention,)
        mapping = dict(
            pd_number="number",
            pd_title="title",
            partner="agreement.partner.organization.name",
            partner_cso_type="agreement.partner.organization.cso_type",
            partner_type="agreement.partner.organization.organization_type",
            partner_vendor_number="agreement.partner.organization.vendor_number",
        )


class InterventionEPDLoader(EtoolsLoader):
    pass


class InterventionEPD(InterventionSimpleAbstract, EtoolsDataMartModel):
    budget_owner = models.CharField(max_length=150, blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    date_sent_to_partner = models.DateField(blank=True, null=True)
    equity_narrative = models.TextField(blank=True, null=True)
    equity_rating = models.CharField(max_length=50, blank=True, null=True)
    gender_narrative = models.TextField(blank=True, null=True)
    gender_rating = models.CharField(max_length=50, blank=True, null=True)
    hq_support_cost = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    implementation_strategy = models.TextField(blank=True, null=True)
    ip_program_contribution = models.TextField(blank=True, null=True)
    partner_accepted = models.BooleanField(null=True)
    sustainability_narrative = models.TextField(blank=True, null=True)
    sustainability_rating = models.CharField(max_length=50, blank=True, null=True)
    unicef_accepted = models.BooleanField(null=True)
    unicef_court = models.BooleanField(null=True)
    unicef_review_type = models.CharField(max_length=50, blank=True, null=True)
    humanitarian_flag = models.BooleanField(null=True)
    capacity_development = models.TextField(blank=True, null=True)
    other_info = models.TextField(blank=True, null=True)
    other_partners_involved = models.TextField(blank=True, null=True)
    technical_guidance = models.TextField(blank=True, null=True)
    cash_transfer_modalities = models.TextField(blank=True, null=True)  # This field type is a guess.
    cancel_justification = models.TextField(blank=True, null=True)
    date_partnership_review_performed = models.DateField(blank=True, null=True)
    accepted_on_behalf_of_partner = models.BooleanField(null=True)
    activation_protocol = models.TextField(blank=True, null=True)
    confidential = models.BooleanField(null=True)

    loader = InterventionEPDLoader()

    class Meta:
        ordering = ("country_name", "pd_title")
        verbose_name = "Intervention ePD"

    class Options:
        source = PartnersIntervention
        queryset = lambda: PartnersIntervention.objects.all()
        mapping = dict(
            **InterventionSimpleAbstract.Options.mapping,
            budget_owner="budget_owner.username",
        )
