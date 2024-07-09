from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import JSONField, Prefetch

from celery.utils.log import get_task_logger

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.models import Location
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention import InterventionAbstract, InterventionLoader
from etools_datamart.apps.sources.etools.enrichment.consts import PartnersInterventionConst, TravelType
from etools_datamart.apps.sources.etools.models import (
    FundsFundsreservationheader,
    models,
    PartnersFiletype,
    PartnersIntervention,
    PartnersInterventionamendment,
    PartnersInterventionattachment,
    PartnersInterventionbudget,
    PartnersInterventionplannedvisits,
    PartnersInterventionresultlink,
    PartnersPartnerorganization,
    ReportsAppliedindicator,
    ReportsLowerresult,
    ReportsResult,
    T2FTravelactivity,
)

logger = get_task_logger(__name__)


class InterventionBudgetLoader(InterventionLoader):
    def get_queryset(self):
        return (
            PartnersInterventionbudget.objects.exclude(intervention__isnull=True)
            .select_related(
                "intervention",
                # "intervention__unicef_signatory",
                "intervention__agreement",
                "intervention__agreement__partner",
                "intervention__agreement__partner__organization",
                "intervention__country_programme",
            )
            .prefetch_related(
                Prefetch(
                    "intervention__FundsFundsreservationheader_intervention",
                    queryset=FundsFundsreservationheader.objects.all(),
                ),
                # Prefetch(
                #    "intervention__agreement__partner__PartnersAgreement_partner",
                #    queryset=PartnersPartnerorganization.objects.all(),
                # ),
                Prefetch(
                    "intervention__PartnersInterventionamendment_intervention",
                    queryset=PartnersInterventionamendment.objects.all().order_by("signed_date"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionattachment_intervention",
                    queryset=PartnersInterventionattachment.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionplannedvisits_intervention",
                    queryset=PartnersInterventionplannedvisits.objects.filter(year=self.context["today"].year),
                ),
                Prefetch(
                    "intervention__PartnersInterventionresultlink_intervention__ReportsLowerresult_result_link__ReportsAppliedindicator_lower_result",
                    queryset=ReportsAppliedindicator.objects.all(),
                ),
                Prefetch(
                    "intervention__T2FTravelactivity_partnership",
                    queryset=T2FTravelactivity.objects.filter(
                        travel_type=TravelType.PROGRAMME_MONITORING,
                        travels__status="completed",
                        date__isnull=False,
                    ).order_by("date"),
                ),
                Prefetch(
                    "intervention__country_programme__ReportsResult_country_programme",
                    queryset=ReportsResult.objects.all(),
                ),
            )
        )

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")
        qs = self.get_queryset().exclude(intervention__isnull=True)

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for record in page.object_list:
                filters = self.config.key(self, record)
                values = self.get_values(record.intervention)
                values["source_id"] = record.id
                values["budget_cso_contribution"] = record.partner_contribution_local
                values["budget_unicef_cash"] = record.unicef_cash_local
                # values["budget_total_unfunded"] = record.total_unfunded
                values["budget_total"] = record.total_local
                values["budget_currency"] = record.currency
                values["budget_unicef_supply"] = record.in_kind_amount_local
                op = self.process_record(filters, values)
                self.increment_counter(op)

    def get_fr_numbers(self, record: PartnersInterventionbudget, values: dict, **kwargs):
        data = []
        ret = []

        for item in record.FundsFundsreservationheader_intervention.all():
            ret.append(item.fr_number)
            data.append(
                dict(
                    fr_number=item.fr_number,
                    vendor_code=item.vendor_code,
                    fr_type=item.fr_type,
                    currency=item.currency,
                )
            )
        values["fr_numbers_data"] = data
        return ", ".join(ret)


class InterventionBudget(InterventionAbstract, EtoolsDataMartModel):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    budget_cso_contribution = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_currency = models.CharField(max_length=5, blank=True, null=True)
    budget_total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # budget_total_unfunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_supply = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    fr_numbers = models.TextField(max_length=100, blank=True, null=True)
    fr_numbers_data = JSONField(blank=True, null=True, default=dict)

    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True, default=dict)

    loader = InterventionBudgetLoader()

    class Meta:
        ordering = ("-created",)

    class Options(InterventionAbstract.Options):
        model = PartnersInterventionbudget
        depends = (Location,)
        key = lambda loader, record: dict(schema_name=loader.context["country"].schema_name, source_id=record.pk)
        mapping = dict(
            agreement_reference_number="agreement.reference_number",
            amendment_types="-",
            attachment_types="-",
            clusters="-",
            contingency_pd="=",
            country_programme="country_programme.name",
            country_programme_id="country_programme.pk",
            cp_outputs="-",
            created="=",
            cso_type="agreement.partner.organization.cso_type",
            currency="agreement.partner.currency",
            days_from_submission_to_signature="-",
            days_from_prc_review_to_signature="-",
            end_date="end",
            fr_number="-",
            outstanding_amt_local="-",
            in_kind_amount="agreement.partner.in_kind_amount",
            in_kind_amount_local="agreement.partner.in_kind_amount_local",
            intervention_id="id",
            last_amendment_date="i",
            last_pv_date="-",
            location="i",
            number_of_amendments="i",
            number_of_attachments="i",
            offices="-",
            offices_data="i",
            partner_authorized_officer_signatory_id="partner_authorized_officer_signatory.pk",
            partner_contribution="agreement.partner.partner_contribution",
            partner_contribution_local="agreement.partner.partner_contribution_local",
            partner_focal_points="-",
            partner_focal_points_data="i",
            partner_id="-",
            partner_name="agreement.partner.organization.name",
            partner_sea_risk_rating="i",
            partner_signatory_email="partner_authorized_officer_signatory.email",
            partner_signatory_first_name="partner_authorized_officer_signatory.first_name",
            partner_signatory_last_name="partner_authorized_officer_signatory.last_name",
            partner_signatory_phone="partner_authorized_officer_signatory.phone",
            partner_signatory_title="partner_authorized_officer_signatory.title",
            partner_source_id="agreement.partner.id",
            partner_type="agreement.partner.organization.organization_type",
            partner_vendor_number="agreement.partner.organization.vendor_number",
            planned_programmatic_visits="-",
            prc_review_document="-",
            sections="-",
            start_date="start",
            status="=",
            total="agreement.partner.total",
            # has_unfunded_cash="PartnersInterventionbudget_intervention.has_unfunded_cash",
            # total_unfunded="PartnersInterventionbudget_intervention.total_unfunded",
            total_local="agreement.partner.total_local",
            unicef_cash="agreement.partner.unicef_cash",
            unicef_cash_local="agreement.partner.unicef_cash_local",
            unicef_focal_points="-",
            unicef_focal_points_data="i",
            # unicef_signatory_email='unicef_signatory.email',
            # unicef_signatory_first_name='unicef_signatory.first_name',
            # unicef_signatory_id='unicef_signatory.pk',
            # unicef_signatory_last_name='unicef_signatory.last_name',
            updated="modified",
            cfei_number="=",
        )
