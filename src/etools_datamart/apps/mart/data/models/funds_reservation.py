from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.sources.etools.models import FundsFundsreservationitem

from .base import EtoolsDataMartModel
from .intervention import Intervention


class FundsReservationLoader(EtoolsLoader):
    """
    --
    SET search_path = public,##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count"
    FROM "funds_fundsreservationitem";


    SELECT '##COUNTRY##' AS __schema,
          "funds_fundsreservationitem"."id",
          "funds_fundsreservationitem"."fr_ref_number",
          "funds_fundsreservationitem"."line_item",
          "funds_fundsreservationitem"."wbs",
          "funds_fundsreservationitem"."grant_number",
          "funds_fundsreservationitem"."fund",
          "funds_fundsreservationitem"."overall_amount",
          "funds_fundsreservationitem"."overall_amount_dc",
          "funds_fundsreservationitem"."due_date",
          "funds_fundsreservationitem"."line_item_text",
          "funds_fundsreservationitem"."fund_reservation_id",
          "funds_fundsreservationitem"."created",
          "funds_fundsreservationitem"."modified",
          "funds_fundsreservationitem"."donor",
          "funds_fundsreservationitem"."donor_code",

          "funds_fundsreservationheader"."id",
          "funds_fundsreservationheader"."vendor_code",
          "funds_fundsreservationheader"."fr_number",
          "funds_fundsreservationheader"."document_date",
          "funds_fundsreservationheader"."fr_type",
          "funds_fundsreservationheader"."currency",
          "funds_fundsreservationheader"."document_text",
          "funds_fundsreservationheader"."start_date",
          "funds_fundsreservationheader"."end_date",
          "funds_fundsreservationheader"."actual_amt",
          "funds_fundsreservationheader"."intervention_id",
          "funds_fundsreservationheader"."intervention_amt",
          "funds_fundsreservationheader"."outstanding_amt",
          "funds_fundsreservationheader"."total_amt",
          "funds_fundsreservationheader"."created",
          "funds_fundsreservationheader"."modified",
          "funds_fundsreservationheader"."actual_amt_local",
          "funds_fundsreservationheader"."outstanding_amt_local",
          "funds_fundsreservationheader"."total_amt_local",
          "funds_fundsreservationheader"."multi_curr_flag",
          "funds_fundsreservationheader"."completed_flag",
          "funds_fundsreservationheader"."delegated"
    FROM "funds_fundsreservationitem"
    INNER JOIN "funds_fundsreservationheader" ON ("funds_fundsreservationitem"."fund_reservation_id" = "funds_fundsreservationheader"."id")
    ORDER BY "funds_fundsreservationitem"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_intervention"."id",
           "partners_intervention"."created",
           "partners_intervention"."modified",
           "partners_intervention"."document_type",
           "partners_intervention"."number",
           "partners_intervention"."title",
           "partners_intervention"."status",
           "partners_intervention"."start",
           "partners_intervention"."end",
           "partners_intervention"."submission_date",
           "partners_intervention"."submission_date_prc",
           "partners_intervention"."review_date_prc",
           "partners_intervention"."prc_review_document",
           "partners_intervention"."signed_by_unicef_date",
           "partners_intervention"."signed_by_partner_date",
           "partners_intervention"."population_focus",
           "partners_intervention"."agreement_id",
           "partners_intervention"."unicef_signatory_id",
           "partners_intervention"."signed_pd_document",
           "partners_intervention"."country_programme_id",
           "partners_intervention"."contingency_pd",
           "partners_intervention"."metadata",
           "partners_intervention"."in_amendment",
           "partners_intervention"."reference_number_year",
           "partners_intervention"."activation_letter",
           "partners_intervention"."termination_doc",
           "partners_intervention"."cfei_number",
           "partners_intervention"."budget_owner_id",
           "partners_intervention"."context",
           "partners_intervention"."date_sent_to_partner",
           "partners_intervention"."equity_narrative",
           "partners_intervention"."equity_rating",
           "partners_intervention"."gender_narrative",
           "partners_intervention"."gender_rating",
           "partners_intervention"."hq_support_cost",
           "partners_intervention"."implementation_strategy",
           "partners_intervention"."ip_program_contribution",
           "partners_intervention"."partner_accepted",
           "partners_intervention"."sustainability_narrative",
           "partners_intervention"."sustainability_rating",
           "partners_intervention"."unicef_accepted",
           "partners_intervention"."unicef_court",
           "partners_intervention"."unicef_review_type",
           "partners_intervention"."humanitarian_flag",
           "partners_intervention"."capacity_development",
           "partners_intervention"."other_info",
           "partners_intervention"."other_partners_involved",
           "partners_intervention"."technical_guidance",
           "partners_intervention"."cash_transfer_modalities",
           "partners_intervention"."cancel_justification",
           "partners_intervention"."date_partnership_review_performed",
           "partners_intervention"."accepted_on_behalf_of_partner",
           "partners_intervention"."activation_protocol",
           "partners_intervention"."confidential",
           "partners_intervention"."has_activities_involving_children",
           "partners_intervention"."has_data_processing_agreement",
           "partners_intervention"."has_special_conditions_for_construction",
           "partners_intervention"."final_review_approved",
           "partners_intervention"."other_details",
           "partners_intervention"."partner_authorized_officer_signatory_id"
    FROM "partners_intervention"
    WHERE "partners_intervention"."id" IN ( ## LIST OF "funds_fundsreservationheader"."intervention_id" IN THE PAGE##);
    """

    def get_intervention(self, record, values, **kwargs):
        if record.fund_reservation.intervention:
            try:
                return Intervention.objects.get(
                    schema_name=self.context["country"].schema_name, source_id=record.fund_reservation.intervention.pk
                )
            except Intervention.DoesNotExist:
                pass


class FundsReservation(EtoolsDataMartModel):
    # header
    vendor_code = models.CharField(max_length=20)
    fr_number = models.CharField(max_length=20)
    document_date = models.DateField(blank=True, null=True)
    fr_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    document_text = models.CharField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    actual_amt = models.DecimalField(max_digits=20, decimal_places=2)
    intervention_amt = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_amt = models.DecimalField(max_digits=20, decimal_places=2)
    total_amt = models.DecimalField(max_digits=20, decimal_places=2)
    # created = models.DateTimeField()
    # modified = models.DateTimeField()
    actual_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    total_amt_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    multi_curr_flag = models.BooleanField()
    completed_flag = models.BooleanField(default=None, blank=True, null=True)
    delegated = models.BooleanField(default=None, blank=True, null=True)

    # item
    fr_ref_number = models.CharField(max_length=30)
    line_item = models.SmallIntegerField()
    wbs = models.CharField(max_length=30)
    grant_number = models.CharField(max_length=20)
    fund = models.CharField(max_length=10)
    overall_amount = models.DecimalField(max_digits=20, decimal_places=2)
    overall_amount_dc = models.DecimalField(max_digits=20, decimal_places=2)
    due_date = models.DateField(blank=True, null=True)
    line_item_text = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    donor = models.CharField(max_length=256, blank=True, null=True)
    donor_code = models.CharField(max_length=30, blank=True, null=True)
    intervention_title = models.CharField(max_length=256, blank=True, null=True)
    pd_reference_number = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )

    # extras
    pd_ssfa_number = models.CharField(max_length=64, null=True)

    # internals
    source_id = models.IntegerField()
    source_intervention_id = models.IntegerField()
    intervention = models.ForeignKey(Intervention, models.SET_NULL, related_name="funds", blank=True, null=True)

    loader = FundsReservationLoader()

    class Meta:
        unique_together = (("schema_name", "source_id"),)
        verbose_name = "Funds Reservation"

    class Options:
        depends = (Intervention,)
        source = FundsFundsreservationitem
        queryset = lambda: FundsFundsreservationitem.objects.select_related("fund_reservation")
        last_modify_field = "modified"
        # key = lambda loader, record: dict(country_name=loader.context['country'].name,
        #                                   schema_name=loader.context['country'].schema_name,
        #                                   fr_number=record.fund_reservation.fr_number)

        mapping = dict(
            vendor_code="fund_reservation.vendor_code",
            fr_number="fund_reservation.fr_number",
            document_date="fund_reservation.document_date",
            pd_ssfa_number="fund_reservation.number",
            fr_type="fund_reservation.fr_type",
            currency="fund_reservation.currency",
            document_text="fund_reservation.document_text",
            start_date="fund_reservation.start_date",
            end_date="fund_reservation.end_date",
            actual_amt="fund_reservation.actual_amt",
            intervention_amt="fund_reservation.intervention_amt",
            outstanding_amt="fund_reservation.outstanding_amt",
            total_amt="fund_reservation.total_amt",
            actual_amt_local="fund_reservation.actual_amt_local",
            total_amt_local="fund_reservation.total_amt_local",
            outstanding_amt_local="fund_reservation.outstanding_amt_local",
            multi_curr_flag="fund_reservation.multi_curr_flag",
            completed_flag="fund_reservation.completed_flag",
            intervention_title="fund_reservation.intervention.title",
            delegated="i",
            source_id="id",
            source_intervention_id="fund_reservation.id",
            wbs="wbs",
            fund="fund",
            pd_reference_number="fund_reservation.intervention.reference_number",
        )
