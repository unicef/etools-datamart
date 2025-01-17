from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.sources.etools.models import FundsFundsreservationheader

from .base import EtoolsDataMartModel
from .intervention import Intervention


class FundsReservationHeader(EtoolsDataMartModel):
    """
    --
    SET search_path = public,##COUNTRY##;

    -- Count
    SELECT COUNT(*) AS "__count" FROM "funds_fundsreservationheader";

    --
    SELECT '##COUNTRY##' AS __schema,
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
           "funds_fundsreservationheader"."delegated",

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
    FROM "funds_fundsreservationheader"
    LEFT OUTER JOIN "partners_intervention" ON ("funds_fundsreservationheader"."intervention_id" = "partners_intervention"."id")
    ORDER BY "funds_fundsreservationheader"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;
    """

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
    created = models.DateTimeField()
    modified = models.DateTimeField()
    actual_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    total_amt_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    multi_curr_flag = models.BooleanField()
    completed_flag = models.BooleanField(default=None, blank=True, null=True)
    delegated = models.BooleanField(default=None, blank=True, null=True)
    pd_reference_number = models.CharField(max_length=256, blank=True, null=True)

    loader = EtoolsLoader()

    class Meta:
        unique_together = (("schema_name", "fr_number", "vendor_code"),)
        verbose_name = "Funds Reservation Header"

    class Options:
        depends = (Intervention,)
        source = FundsFundsreservationheader
        queryset = lambda: FundsFundsreservationheader.objects.select_related("intervention")
        last_modify_field = "modified"

        mapping = dict(
            pd_reference_number="intervention.reference_number",
        )
