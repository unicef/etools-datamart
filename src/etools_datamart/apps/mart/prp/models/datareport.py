from datetime import timedelta

from django.db import models
from django.db.models import F, Q

from constance import config
from dateutil.utils import today

from etools_datamart.apps.mart.prp.base import PrpDataMartModel
from etools_datamart.apps.mart.prp.models.base import PrpBaseLoader
from etools_datamart.apps.sources.source_prp.models import IndicatorIndicatorlocationdata, UnicefLowerleveloutput


class DataReportLoader(PrpBaseLoader):
    def get_queryset(self):
        qs = (
            IndicatorIndicatorlocationdata.objects.filter(
                modified__gte=today() - timedelta(config.DEFAULT_ARCHIVE_DELTA),
            )
            .exclude(
                Q(indicator_report__progress_report__isnull=True)
                | Q(indicator_report__progress_report__status__in=["Due", "Ove", "Sen"])
            )
            .select_related(
                "indicator_report",
                "indicator_report__progress_report",
                "indicator_report__progress_report__programme_document",
                "indicator_report__progress_report__programme_document__partner",
                "indicator_report__progress_report__programme_document__workspace",
                "indicator_report__progress_report__submitted_by",
                "indicator_report__reportable",
                "indicator_report__reportable__blueprint",
                "indicator_report__reportable__parent_indicator",
                "location",
            )
            .annotate(
                report_type=F("indicator_report__progress_report__report_type"),
                country_name=F("indicator_report__progress_report__programme_document__workspace__title"),
                business_area=F("indicator_report__progress_report__programme_document__workspace__business_area_code"),
                partner_name=F("indicator_report__progress_report__programme_document__partner__title"),
                partner_vendor_number=F(
                    "indicator_report__progress_report__programme_document__partner__vendor_number"
                ),
                etools_intervention_id=F("indicator_report__progress_report__programme_document__external_id"),
                prp_intervention_id=F("indicator_report__progress_report__programme_document__id"),
                intervention_reference_number=F(
                    "indicator_report__progress_report__programme_document__reference_number"
                ),
                submitted_by=F("indicator_report__progress_report__submitted_by__username"),
                performance_indicator=F("indicator_report__reportable__blueprint__title"),
                target=F("indicator_report__reportable__target"),
                cluster_indicator=F("indicator_report__reportable__is_cluster_indicator"),
                indicator_type=F("indicator_report__reportable__blueprint__display_type"),
                high_frequency=F("indicator_report__reportable__is_unicef_hf_indicator"),
                means_of_verification=F("indicator_report__reportable__means_of_verification"),
                achievement_in_reporting_period=F("indicator_report__total"),
                total_cumulative_progress=F("indicator_report__reportable__total"),
                report_number=F("indicator_report__progress_report__report_number"),
                due_date=F("indicator_report__progress_report__due_date"),
                reporting_period_start_date=F("indicator_report__progress_report__start_date"),
                reporting_period_end_date=F("indicator_report__progress_report__end_date"),
                reporting_period_due_date=F("indicator_report__progress_report__due_date"),
                report_submission_date=F("indicator_report__progress_report__submission_date"),
                narrative=F("indicator_report__progress_report__narrative"),
                report_status=F("indicator_report__report_status"),
                pd_output_title=F("indicator_report__reportable__parent_indicator__blueprint__title"),
                pd_output_progress_status=F("indicator_report__overall_status"),
                pd_output_narrative_assessment=F("indicator_report__narrative_assessment"),
                calculation_method_across_location=F(
                    "indicator_report__reportable__blueprint__calculation_formula_across_locations"
                ),
                calculation_method_across_reporting_periods=F(
                    "indicator_report__reportable__blueprint__calculation_formula_across_periods"
                ),
                current_location=F("location__name"),
                p_code=F("location__p_code"),
                admin_level=F("location__admin_level"),
            )
        )
        return qs

    def get_values(self, record: IndicatorIndicatorlocationdata):
        values = super().get_values(record)
        ct = record.indicator_report.reportable.content_type
        if ct.model == "lowerleveloutput":
            ll = UnicefLowerleveloutput.objects.select_related("cp_output", "cp_output__programme_document").get(
                id=record.indicator_report.reportable.object_id
            )
            values["pd_output_title"] = ll.title
            values["cp_output"] = ll.cp_output.title
            values["etools_cp_output_id"] = ll.cp_output.external_cp_output_id
            values["programme_document"] = ll.cp_output.programme_document.reference_number
            pd2sections = (
                ll.cp_output.programme_document.UnicefProgrammedocumentSections_programmedocument.all().select_related(
                    "section"
                )
            )
            values["section"] = ", ".join([pd2section.section.name for pd2section in pd2sections])

        return values

    def get_locations(self, record: IndicatorIndicatorlocationdata, values, **kwargs):
        locs = []
        qs = record.indicator_report.reportable.IndicatorReportablelocationgoal_reportable.select_related("location")
        for goal in qs:
            locs.append(
                dict(
                    source_id=goal.location.id,
                    name=goal.location.name,
                    pcode=goal.location.p_code,
                    level=goal.location.admin_level,
                    levelname=goal.location.admin_level_name,
                )
            )
        values["locations_data"] = locs
        return ", ".join([loc["name"] for loc in locs])

    # def get_disaggregation(self, record: IndicatorIndicatorlocationdata, values, **kwargs):
    #     # get disaggregation data and replace keys with disaggration value
    #     disaggKeyValues = {}
    #     for pk, value in IndicatorDisaggregationvalue.objects.values_list("pk", "value").all():
    #         try:
    #             pk = int(pk)
    #         except TypeError:
    #             # probably a None, so we can ignore
    #             pass
    #         disaggKeyValues[pk] = value
    #     disagg = {}
    #     disaggregation = json.loads(record.disaggregation)
    #     for k, v in disaggregation.items():
    #         k = literal_eval(k)
    #         if len(k):
    #             nk = []
    #             for i in k:
    #                 try:
    #                     nk.append(disaggKeyValues[int(i)])
    #                 except KeyError:
    #                     nk.append(int(i))
    #             k = tuple(nk)
    #         disagg[str(k)] = v
    #     return disagg


class DataReport(PrpDataMartModel):
    # | indicator_report | idl.indicator_report |
    indicator_report = models.CharField(max_length=2048, blank=True, null=True)
    # | progres_report | indicator_report.progres_report |
    progress_report = models.CharField(max_length=2048, blank=True, null=True)
    report_type = models.CharField(max_length=256, blank=True, null=True)
    # | programme_document | r.lower_level_output.cp_output.programme_document |
    programme_document = models.CharField(max_length=2048, blank=True, null=True)

    # |  # indicator data|
    # | country_name | programme_document.workspace.title |
    country_name = models.CharField(max_length=2048, blank=True, null=True)
    # | business_area | programme_document.workspace.business_area_code |
    business_area = models.CharField(max_length=2048, blank=True, null=True)
    # | partner_name | programme_document.partner.title |
    partner_name = models.CharField(max_length=2048, blank=True, null=True)
    # | partner_vendor_number | programme_document.partner.vendor_number |
    partner_vendor_number = models.CharField(max_length=2048, blank=True, null=True)
    # | etools_intervention_id | programme_document.external_id |
    etools_intervention_id = models.CharField(max_length=2048, blank=True, null=True)
    # | prp_intervention_id | programme_document.id |
    prp_intervention_id = models.CharField(max_length=2048, blank=True, null=True)
    # | country_programme | "NA -> available in etools under intervention.country_programme" |
    # country_programme = models.CharField(max_length=2048, blank=True, null=True)
    # | cp_output | r.lower_level_output.cp_output. |
    cp_output = models.CharField(max_length=2048, blank=True, null=True)
    # | intervention_reference_number | programme_document.reference_number |
    # intervention_reference_number = models.CharField(max_length=2048, blank=True, null=True)
    # # | intervention_reference_number | programme_document.reference_number |
    intervention_reference_number = models.CharField(max_length=2048, blank=True, null=True)
    # | cp_output | "NA in PRP - > Available in etools under reports.Results where the id is found using prp field r.lower_level_output.cp_output.external_cp_output_id" |
    # cp_output = models.CharField(max_length=2048, blank=True, null=True)
    # | etools_cp_output_id | r.lower_level_output.cp_output.external_cp_output_id |
    etools_cp_output_id = models.CharField(max_length=2048, blank=True, null=True)
    # | cp_output_indicators | "NA in PRP - > Available in etools result|partners.InterventionResultLink.filter(id|prp_id) where the prp_id is found using prp field r.lower_level_output.cp_output.external_id and then: indicators | [i.name for i in result.ram_indicators.all()]." |
    cp_output_indicators = models.CharField(max_length=2048, blank=True, null=True)
    # | etools_cp_output_indicators_id | "NA in PRP - > Available in etools result|partners.InterventionResultLink.filter(id|prp_id) where the prp_id is found using prp field r.lower_level_output.cp_output.external_id and then: indicators | [i.id for i in result.ram_indicators.all()]." |
    etools_cp_output_indicators_id = models.CharField(max_length=2048, blank=True, null=True)
    # | pd_result | r.lower_level_output.title |
    pd_result = models.CharField(max_length=2048, blank=True, null=True)
    # | etools_pd_result_id | r.lower_level_output.external_id |
    etools_pd_result_id = models.CharField(max_length=2048, blank=True, null=True)
    # | performance_indicator | r.blueprint.title |
    performance_indicator = models.CharField(max_length=2048, blank=True, null=True)
    # | section | "NA in PRP -> etools result | AppliedIndicator.objects.get(id|my_id) where my_id | r.external_id -> section | result.section|
    section = models.CharField(max_length=2048, blank=True, null=True)
    # | cluster_indicator | r.is_cluster_indicator |
    cluster_indicator = models.CharField(max_length=2048, blank=True, null=True)
    # | indicator_type | r.blueprint.display_type |
    indicator_type = models.CharField(max_length=2048, blank=True, null=True)
    # | baseline | r.calculated_baseline  # bbusiness logic copy here|
    baseline = models.CharField(max_length=2048, blank=True, null=True)
    # | target | r.calculated_target  # business logic copy here|
    target = models.CharField(max_length=2048, blank=True, null=True)
    # | high_frequency | r.is_unicef_hf_indicator |
    high_frequency = models.CharField(max_length=2048, blank=True, null=True)
    report_status = models.CharField(max_length=256, blank=True, null=True)
    # | means_of_verification | r.means_of_verification |
    means_of_verification = models.CharField(max_length=2048, blank=True, null=True)
    # | locations | r.lower_level_output.locations.all()  # magic by stefano|
    locations = models.TextField(blank=True, null=True)
    locations_data = models.JSONField(blank=True, null=True)
    # |  # progress data|
    # | report_number | progres_report.report_number |
    report_number = models.CharField(max_length=2048, blank=True, null=True)
    # | due_date | progres_report.due_date |
    due_date = models.DateField(blank=True, null=True)
    # | reporting_period_start_date | progres_report.start_date |
    reporting_period_start_date = models.DateField(blank=True, null=True)
    # | reporting_period_end_date | progres_report.end_date |
    reporting_period_end_date = models.DateField(blank=True, null=True)
    # | reporting_period_due_date | progres_report.due_date |
    reporting_period_due_date = models.DateField(blank=True, null=True)
    # | report_submission_date | progres_report.submission_date |
    report_submission_date = models.DateField(blank=True, null=True)
    # | submitted_by | progres_report.submitted_by.first_name + progres_report.submitted_by.last_name + progres_report.submitted_by.email |
    submitted_by = models.CharField(max_length=2048, blank=True, null=True)
    # | face_attachment | "nope" |x
    # | attachment_1 | "nope" |
    # | attachment_2 | "nope" |
    # | narrative | progres_report.narrative |
    narrative = models.CharField(max_length=2048, blank=True, null=True)
    pd_output_title = models.CharField(max_length=2048, blank=True, null=True)
    # | pd_output_progress_status | indicator_report.overall_status |
    pd_output_progress_status = models.CharField(max_length=2048, blank=True, null=True)
    # | pd_output_narrative_assessment | indicator_report.narrative_assessment |
    pd_output_narrative_assessment = models.TextField(blank=True, null=True)
    # | calculation_method_across_location | r.blueprint.calculation_formula_across_locations |
    calculation_method_across_location = models.CharField(max_length=2048, blank=True, null=True)
    # | calculation_method_across_reporting_periods | r.blueprint.calculation_formula_across_periods |
    calculation_method_across_reporting_periods = models.CharField(max_length=2048, blank=True, null=True)
    # | current_location | idl.location  # this is current location data|
    current_location = models.CharField(max_length=2048, blank=True, null=True)
    # | previous_location_progress | idl.previous_location_data  # this is custom code copy from indicator.models L1063|
    previous_location_progress = models.CharField(max_length=2048, blank=True, null=True)
    # | total_cummulative_progress_in_location | "instruct user to figure out" |
    total_cumulative_progress_in_location = models.CharField(max_length=2048, blank=True, null=True)
    # total_cumulative_progress | reportable.total["c"] |
    total_cumulative_progress = models.CharField(max_length=2048, blank=True, null=True)
    achievement_in_reporting_period = models.CharField(max_length=2048, blank=True, null=True)
    disaggregation = models.JSONField(blank=True, null=True)
    p_code = models.CharField(max_length=32, blank=True, null=True)
    admin_level = models.SmallIntegerField(null=True)

    loader = DataReportLoader()

    class Meta:
        app_label = "prp"

    def __str__(self):
        return f"{self.country_name} | {self.partner_name} | {self.cp_output} | {self.intervention_reference_number} | {self.pd_result}"

    class Options:
        archive_delta = config.DEFAULT_ARCHIVE_DELTA
        archive_field = "last_modify_date"
        mapping = {
            "indicator_report": "indicator_report_title",
            "programme_document": "i",
            "etools_cp_output_id": "i",
            "locations": "-",
            "section": "i",
        }
