from django.conf import settings
from django.core.paginator import Paginator
from django.db import models
from django.db.models import JSONField

from celery.utils.log import get_task_logger

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.fields import SafeDecimal
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.mixins import NestedLocationLoaderMixin, NestedLocationMixin
from etools_datamart.apps.sources.etools.models import PartnersIntervention, ReportsAppliedindicator, ReportsLowerresult

logger = get_task_logger(__name__)


def get_pd_output_names(obj: PartnersIntervention):
    return [ll.name for rl in obj.result_links.all() for ll in rl.ll_results.all()]


class ReportIndicatorLoader(NestedLocationLoaderMixin, EtoolsLoader):
    """
    --
    SET search_path = public,afghanistan;

    --
    SELECT COUNT(*) AS "__count"
    FROM "reports_appliedindicator";

    --
    SELECT '##COUNTRY##' AS __schema,
           "reports_appliedindicator"."id",
           "reports_appliedindicator"."context_code",
           "reports_appliedindicator"."assumptions",
           "reports_appliedindicator"."total",
           "reports_appliedindicator"."indicator_id",
           "reports_appliedindicator"."lower_result_id",
           "reports_appliedindicator"."means_of_verification",
           "reports_appliedindicator"."cluster_indicator_id",
           "reports_appliedindicator"."cluster_indicator_title",
           "reports_appliedindicator"."cluster_name",
           "reports_appliedindicator"."created",
           "reports_appliedindicator"."modified",
           "reports_appliedindicator"."response_plan_name",
           "reports_appliedindicator"."section_id",
           "reports_appliedindicator"."is_active",
           "reports_appliedindicator"."is_high_frequency",
           "reports_appliedindicator"."baseline",
           "reports_appliedindicator"."denominator_label",
           "reports_appliedindicator"."label",
           "reports_appliedindicator"."measurement_specifications",
           "reports_appliedindicator"."numerator_label",
           "reports_appliedindicator"."target",

           "reports_indicatorblueprint"."id",
           "reports_indicatorblueprint"."title",
           "reports_indicatorblueprint"."description",
           "reports_indicatorblueprint"."code",
           "reports_indicatorblueprint"."subdomain",
           "reports_indicatorblueprint"."disaggregatable",
           "reports_indicatorblueprint"."unit",
           "reports_indicatorblueprint"."calculation_formula_across_locations",
           "reports_indicatorblueprint"."calculation_formula_across_periods",
           "reports_indicatorblueprint"."created",
           "reports_indicatorblueprint"."display_type",
           "reports_indicatorblueprint"."modified",

           "reports_lowerresult"."id",
           "reports_lowerresult"."name",
           "reports_lowerresult"."code",
           "reports_lowerresult"."result_link_id",
           "reports_lowerresult"."created",
           "reports_lowerresult"."modified",
           "reports_lowerresult"."is_active",

           "partners_interventionresultlink"."id",
           "partners_interventionresultlink"."cp_output_id",
           "partners_interventionresultlink"."intervention_id",
           "partners_interventionresultlink"."created",
           "partners_interventionresultlink"."modified",
           "partners_interventionresultlink"."code",

           "reports_result"."id",
           "reports_result"."name",
           "reports_result"."code",
           "reports_result"."result_type_id",
           "reports_result"."sector_id",
           "reports_result"."gic_code",
           "reports_result"."gic_name",
           "reports_result"."humanitarian_tag",
           "reports_result"."level",
           "reports_result"."lft",
           "reports_result"."parent_id",
           "reports_result"."rght",
           "reports_result"."sic_code",
           "reports_result"."sic_name",
           "reports_result"."tree_id",
           "reports_result"."vision_id",
           "reports_result"."wbs",
           "reports_result"."activity_focus_code",
           "reports_result"."activity_focus_name",
           "reports_result"."hidden",
           "reports_result"."from_date",
           "reports_result"."to_date",
           "reports_result"."ram",
           "reports_result"."country_programme_id",
           "reports_result"."created",
           "reports_result"."modified",
           "reports_result"."humanitarian_marker_code",
           "reports_result"."humanitarian_marker_name",
           "reports_result"."programme_area_code",
           "reports_result"."programme_area_name",

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
           "partners_intervention"."partner_authorized_officer_signatory_id",

           "partners_agreement"."id",
           "partners_agreement"."created",
           "partners_agreement"."modified",
           "partners_agreement"."start",
           "partners_agreement"."end",
           "partners_agreement"."agreement_type",
           "partners_agreement"."agreement_number",
           "partners_agreement"."attached_agreement",
           "partners_agreement"."signed_by_unicef_date",
           "partners_agreement"."signed_by_partner_date",
           "partners_agreement"."partner_id",
           "partners_agreement"."signed_by_id",
           "partners_agreement"."status",
           "partners_agreement"."country_programme_id",
           "partners_agreement"."reference_number_year",
           "partners_agreement"."special_conditions_pca",
           "partners_agreement"."terms_acknowledged_by_id",
           "partners_agreement"."partner_manager_id",

           "partners_partnerorganization"."id",
           "partners_partnerorganization"."description",
           "partners_partnerorganization"."address",
           "partners_partnerorganization"."email",
           "partners_partnerorganization"."phone_number",
           "partners_partnerorganization"."alternate_id",
           "partners_partnerorganization"."alternate_name",
           "partners_partnerorganization"."rating",
           "partners_partnerorganization"."core_values_assessment_date",
           "partners_partnerorganization"."vision_synced",
           "partners_partnerorganization"."type_of_assessment",
           "partners_partnerorganization"."last_assessment_date",
           "partners_partnerorganization"."hidden",
           "partners_partnerorganization"."deleted_flag",
           "partners_partnerorganization"."total_ct_cp",
           "partners_partnerorganization"."total_ct_cy",
           "partners_partnerorganization"."blocked",
           "partners_partnerorganization"."city",
           "partners_partnerorganization"."country",
           "partners_partnerorganization"."postal_code",
           "partners_partnerorganization"."shared_with",
           "partners_partnerorganization"."street_address",
           "partners_partnerorganization"."hact_values",
           "partners_partnerorganization"."created",
           "partners_partnerorganization"."modified",
           "partners_partnerorganization"."net_ct_cy",
           "partners_partnerorganization"."reported_cy",
           "partners_partnerorganization"."total_ct_ytd",
           "partners_partnerorganization"."basis_for_risk_rating",
           "partners_partnerorganization"."manually_blocked",
           "partners_partnerorganization"."outstanding_dct_amount_6_to_9_months_usd",
           "partners_partnerorganization"."outstanding_dct_amount_more_than_9_months_usd",
           "partners_partnerorganization"."highest_risk_rating_name",
           "partners_partnerorganization"."highest_risk_rating_type",
           "partners_partnerorganization"."psea_assessment_date",
           "partners_partnerorganization"."sea_risk_rating_name",
           "partners_partnerorganization"."lead_office_id",
           "partners_partnerorganization"."lead_section_id",
           "partners_partnerorganization"."organization_id",

           "organizations_organization"."id",
           "organizations_organization"."created",
           "organizations_organization"."modified",
           "organizations_organization"."name",
           "organizations_organization"."vendor_number",
           "organizations_organization"."organization_type",
           "organizations_organization"."cso_type",
           "organizations_organization"."short_name",
           "organizations_organization"."other",
           "organizations_organization"."parent_id",

           "reports_sector"."id",
           "reports_sector"."name",
           "reports_sector"."description",
           "reports_sector"."alternate_id",
           "reports_sector"."alternate_name",
           "reports_sector"."dashboard",
           "reports_sector"."color",
           "reports_sector"."created",
           "reports_sector"."modified",
           "reports_sector"."active" FROM "reports_appliedindicator"
    LEFT OUTER JOIN "reports_indicatorblueprint" ON ("reports_appliedindicator"."indicator_id" = "reports_indicatorblueprint"."id")
    INNER JOIN "reports_lowerresult" ON ("reports_appliedindicator"."lower_result_id" = "reports_lowerresult"."id")
    INNER JOIN "partners_interventionresultlink" ON ("reports_lowerresult"."result_link_id" = "partners_interventionresultlink"."id")
    LEFT OUTER JOIN "reports_result" ON ("partners_interventionresultlink"."cp_output_id" = "reports_result"."id")
    INNER JOIN "partners_intervention" ON ("partners_interventionresultlink"."intervention_id" = "partners_intervention"."id")
    INNER JOIN "partners_agreement" ON ("partners_intervention"."agreement_id" = "partners_agreement"."id")
    INNER JOIN "partners_partnerorganization" ON ("partners_agreement"."partner_id" = "partners_partnerorganization"."id")
    INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id")
    LEFT OUTER JOIN "reports_sector" ON ("reports_appliedindicator"."section_id" = "reports_sector"."id")
    ORDER BY "reports_appliedindicator"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;


    --
    SELECT ("reports_appliedindicator_locations"."appliedindicator_id") AS "_prefetch_related_val_appliedindicator_id",
           '##COUNTRY##' AS __schema,
           "locations_location"."id",
           "locations_location"."name",
           "locations_location"."latitude",
           "locations_location"."longitude",
           "locations_location"."p_code",
           "locations_location"."point",
           "locations_location"."geom",
           "locations_location"."level",
           "locations_location"."lft",
           "locations_location"."parent_id",
           "locations_location"."rght",
           "locations_location"."tree_id",
           "locations_location"."created",
           "locations_location"."modified",
           "locations_location"."is_active",
           "locations_location"."admin_level",
           "locations_location"."admin_level_name"
    FROM "locations_location" INNER JOIN "reports_appliedindicator_locations" ON ("locations_location"."id" = "reports_appliedindicator_locations"."location_id")
    WHERE "reports_appliedindicator_locations"."appliedindicator_id" IN (##LIST of reports_appliedindicator"."id" in the page##);


    --
    SELECT ("reports_appliedindicator_disaggregation"."appliedindicator_id") AS "_prefetch_related_val_appliedindicator_id",
           '##COUNTRY##' AS __schema,
           "reports_disaggregation"."id",
           "reports_disaggregation"."created",
           "reports_disaggregation"."modified",
           "reports_disaggregation"."name",
           "reports_disaggregation"."active"
    FROM "reports_disaggregation"
    INNER JOIN "reports_appliedindicator_disaggregation" ON ("reports_disaggregation"."id" = "reports_appliedindicator_disaggregation"."disaggregation_id")
    WHERE "reports_appliedindicator_disaggregation"."appliedindicator_id" IN (##LIST of reports_appliedindicator"."id" in the page##);


       --
    SELECT '##COUNTRY##' AS __schema,
           "reports_resulttype"."id",
           "reports_resulttype"."name"
    FROM "reports_resulttype"
    WHERE "reports_resulttype"."id" IN (## List of reports_result"."result_type_id" in the page ## );

    --
    SELECT '##COUNTRY## AS __schema,
           "reports_lowerresult"."id",
           "reports_lowerresult"."name",
           "reports_lowerresult"."code",
           "reports_lowerresult"."result_link_id",
           "reports_lowerresult"."created",
           "reports_lowerresult"."modified",
           "reports_lowerresult"."is_active"
    FROM "reports_lowerresult"
    WHERE "reports_lowerresult"."result_link_id" in (## LIST OF "reports_lowerresult"."result_link_id" IN THE PAGE ##)
    ORDER BY "reports_lowerresult"."modified" ASC;


    """

    location_m2m_field = "locations"

    def get_baseline_denominator(self, record, values, field_name):
        value = SafeDecimal(record.baseline.get("d"))
        if value:
            value._validate_for_field(ReportIndicator._meta.get_field(field_name))
        return value

    def get_baseline_numerator(self, record, values, field_name):
        value = SafeDecimal(record.baseline.get("v"))
        if value:
            value._validate_for_field(ReportIndicator._meta.get_field(field_name))
        return value

    def get_target_value(self, record, values, field_name):
        values["target_denominator"] = SafeDecimal(record.target.get("d"))
        values["target_numerator"] = SafeDecimal(record.target.get("v"))

    def get_disaggregations(self, record, values, field_name):
        ret = []
        for disaggregatio in record.disaggregations.order_by("id"):
            ret.append(dict(source_id=disaggregatio.id, name=disaggregatio.name, active=disaggregatio.active))
        values["disaggregations_data"] = ret
        return ", ".join([dis["name"] for dis in ret])

    def get_pd_outputs(self, record, values, field_name, **kwargs):
        # from
        # etools.applications.partners.serializers.interventions.InterventionMonitorSerializer.get_pd_output_names()
        #     @staticmethod
        #     def get_pd_output_names(obj):
        #         return [ll.name for rl in obj.result_links.all() for ll in rl.ll_results.all()]
        # ---------------------------
        #         record     -->  ReportsIndicatorblueprint (indicator)
        #            |   (lower_result)
        #   ReportsLowerresult
        #            |   (result_link|ll_results )
        #            |                      (intervention|result_links)
        #   PartnersInterventionresultlink  ----------------------------> Intervention
        #            |   (cp_output)
        #        ReportsResult
        #            |   (sector)
        #        ReportsSector
        #
        # result_link: PartnersInterventionresultlink
        # cp_output: ReportsResult
        # pd_output: ReportsLowerresult
        # indicator: ReportsIndicatorblueprint

        # intervention = record.lower_result.result_link.intervention
        #
        # cp_output = record.lower_result.result_link.cp_output
        ll_results = ReportsLowerresult.objects.filter(result_link=record.lower_result.result_link).order_by("modified")
        ret = []
        for pd_output in ll_results.all():
            ret.append(
                dict(
                    last_modify_date=str(pd_output.modified),
                    name=pd_output.name,
                )
            )
        values["pd_outputs_data"] = ret
        return ", ".join([l["name"] for l in ret])

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = self.filter_queryset(self.get_queryset())

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for record in page.object_list:
                filters = self.config.key(self, record)
                values = self.get_values(record)
                op = self.process_record(filters, values)
                self.increment_counter(op)


class ReportIndicator(NestedLocationMixin, EtoolsDataMartModel):
    partner_vendor_number = models.CharField(max_length=100, blank=True, null=True)
    partner_name = models.CharField(max_length=200, null=True)
    assumptions = models.TextField(
        null=True,
        blank=True,
    )
    baseline = JSONField(default=dict, blank=True, null=True)
    baseline_denominator = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=3)
    baseline_numerator = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=3)
    # baseline_denominator = models.IntegerField(blank=True, null=True)
    # baseline_numerator = models.IntegerField(blank=True, null=True)
    cluster_indicator_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    cluster_indicator_title = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
    )
    cluster_name = models.CharField(
        max_length=512,
        blank=True,
        null=True,
    )
    # code = models.CharField(max_length=50, blank=True, null=True)
    context_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    cp_output_name = models.TextField(blank=True, null=True)
    cp_output_type = models.CharField(blank=True, null=True, max_length=150)
    denominator_label = models.CharField(max_length=256, blank=True, null=True)
    disaggregations = models.TextField(blank=True, null=True)
    disaggregations_data = JSONField(blank=True, null=True)
    display_type = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    is_high_frequency = models.BooleanField(default=False, blank=True, null=True)
    label = models.TextField(max_length=4048, blank=True, null=True)
    lower_result_name = models.CharField(max_length=500, blank=True, null=True)
    means_of_verification = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    measurement_specifications = models.TextField(max_length=4048, blank=True, null=True)
    numerator_label = models.CharField(max_length=256, blank=True, null=True)
    pd_outputs = models.TextField(blank=True, null=True)
    pd_outputs_data = JSONField(blank=True, null=True)
    # pd_output_indicator_last_modify_date = models.DateField(blank=True, null=True)
    pd_output_indicator_title = models.CharField(max_length=256, blank=True, null=True)
    # pd_output_name = models.CharField(max_length=256, blank=True, null=True)
    # pd_output_section = models.CharField(max_length=256, blank=True, null=True)
    pd_sffa_reference_number = models.CharField(max_length=256, blank=True, null=True)
    response_plan_name = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
    )
    result_link_intervention = models.IntegerField(blank=True, null=True)
    section_name = models.CharField(max_length=128, blank=True, null=True)
    # source_disaggregation_id = models.IntegerField(blank=True, null=True)
    # source_location_id = models.IntegerField(blank=True, null=True)
    target = JSONField(default=dict, blank=True, null=True)
    target_denominator = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    target_numerator = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    # target_denominator = models.IntegerField(blank=True, null=True)
    # target_numerator = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    total = models.IntegerField(
        null=True,
        blank=True,
        default=0,
    )
    unit = models.CharField(max_length=10, blank=True, null=True)

    loader = ReportIndicatorLoader()

    # # sector = models.ForeignKey(Section, verbose_name=_("Section"), blank=True, null=True, on_delete=models.CASCADE, )
    # # result = models.ForeignKey(        Result, verbose_name=_("Result"), null=True, blank=True, on_delete=models.CASCADE, )
    # name = models.CharField(verbose_name=_("Name"), max_length=1024)
    # code = models.CharField(verbose_name=_("Code"), max_length=50, null=True, blank=True, )
    # # unit = models.ForeignKey(        Unit, verbose_name=_("Unit"), null=True, blank=True, on_delete=models.CASCADE, )
    #
    # total = models.IntegerField(verbose_name=_('UNICEF Target'), null=True, blank=True, )
    # sector_total = models.IntegerField(verbose_name=_('Sector Target'), null=True, blank=True, )
    # current = models.IntegerField(verbose_name=_("Current"), null=True, blank=True, default=0, )
    # sector_current = models.IntegerField(verbose_name=_("Sector Current"), null=True, blank=True, )
    # assumptions = models.TextField(verbose_name=_("Assumptions"), null=True, blank=True, )
    #
    # # RAM Info
    # target = models.CharField(verbose_name=_("Target"), max_length=255, null=True, blank=True, )
    # baseline = models.CharField(verbose_name=_("Baseline"), max_length=255, null=True, blank=True, )
    # ram_indicator = models.BooleanField(verbose_name=_("RAM Indicator"), default=False, )
    # active = models.BooleanField(verbose_name=_("Active"), default=True)
    # view_on_dashboard = models.BooleanField(verbose_name=_("View on Dashboard"), default=False, )

    class Options:
        source = ReportsAppliedindicator
        queryset = lambda: ReportsAppliedindicator.objects.select_related(
            "indicator",
            "section",
            "lower_result",
            "lower_result__result_link",
            "lower_result__result_link__cp_output",
            "lower_result__result_link__intervention",
            "lower_result__result_link__intervention__agreement__partner",
            "lower_result__result_link__intervention__agreement__partner__organization",
        ).prefetch_related("locations", "disaggregations")
        # TODO:  prefetch  reports_lowerresult, locations_location, reports_disaggregation
        mapping = dict(
            partner_name="lower_result.result_link.intervention.agreement.partner.organization.name",
            partner_vendor_number="lower_result.result_link.intervention.agreement.partner.organization.vendor_number",
            baseline_denominator="-",
            baseline_numerator="-",
            cluster_indicator_id="=",
            cluster_indicator_title="=",
            cluster_name="=",
            cp_output_name="lower_result.result_link.cp_output.name",
            cp_output_type="lower_result.result_link.cp_output.result_type.name",
            denominator_label="=",
            disaggregations="-",
            disaggregations_data="i",
            # disaggregation_active='disaggregation.active',
            # disaggregation_name='disaggregation.name',
            display_type="indicator.display_type",
            is_active="=",
            is_high_frequency="=",
            label="=",
            locations="-",
            # locations_data='i',
            lower_result_name="lower_result.name",
            means_of_verification="means_of_verification",
            measurement_specifications="=",
            numerator_label="=",
            # pd_output_indicator_last_modify_date="pd_output_indicator_last_modify_date",
            pd_output_indicator_title="indicator.title,",
            pd_outputs="-",
            pd_outputs_data="i",
            # pd_output_name="N/A",
            # pd_output_section="N/A",
            pd_sffa_reference_number="lower_result.result_link.intervention.number",
            response_plan_name="=",
            result_link_intervention="lower_result.result_link.intervention.pk",
            section_name="section.name",
            # source_disaggregation_id='disaggregation.id',
            # source_location_id='location.id',
            # target_denominator=lambda loader, record: record.target['d'],
            # target_numerator=lambda loader, record: record.target['v'],
            target_denominator="get_target_value",
            target_numerator="get_target_value",
            title="indicator.title",
            unit="indicator.unit",
        )


#
# class ReportIndicatorFlat(ReportIndicator):
#     disaggregation_active = models.BooleanField(default=False)
#     disaggregation_name = models.CharField(max_length=255)
#     pd_output_indicator_last_modify_date = models.DateField(blank=True, null=True)
#     pd_output_indicator_title = models.CharField(max_length=256, blank=True, null=True)
#     pd_output_name = models.CharField(max_length=256, blank=True, null=True)
#     pd_output_section = models.CharField(max_length=256, blank=True, null=True)
#     location_source_id = models.IntegerField(blank=True, null=True)
#     location_name = models.CharField(max_length=254, blank=True, null=True)
#     location_pcode = models.CharField(max_length=32, blank=True, null=True)
#     location_level = models.IntegerField(blank=True, null=True)
#     location_levelname = models.CharField(max_length=32, blank=True, null=True)
#     location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL)


# class ReportIndicatorFlatDisaggregation(ReportIndicator):
#     disaggregation_active = models.BooleanField(default=False)
#     disaggregation_name = models.CharField(max_length=255)
#
#
# class ReportIndicatorFlatPDOutput(ReportIndicator):
#     pd_output_indicator_last_modify_date = models.DateField(blank=True, null=True)
#     pd_output_indicator_title = models.CharField(max_length=256, blank=True, null=True)
#     pd_output_name = models.CharField(max_length=256, blank=True, null=True)
#     pd_output_section = models.CharField(max_length=256, blank=True, null=True)
