"""
IndicatorIndicatorlocationdata -----
1)
Country                         CoreCountry.name
Partner                         PartnerPartner.title
PD                              UnicefProgrammedocument.reference_number
Indicator Target                Reportable.target
Indicator Baseline              Reportable.baseline
Title of Indicator              Reportable.blueprint.title

d. denominatro
v. enumaror
c. calc

2)
Indicator ID                Reportable.id
Indicator Location Name         IndicatorLocationData.location.name
Indicator Location Geo          IndicatorLocationData.location.point
Admin level of location         IndicatorLocationData.location.type.admin_level
Reported Total                  IndicatorLocationData.disaggregation['()']['c']



Country                         CoreCountry.name
Partner                         PartnerPartner.title
PD                              UnicefProgrammedocument.reference_number
Indicator Target                Reportable.target
Indicator Baseline              Reportable.baseline
Title of Indicator              Reportable.blueprint.title
Calculation across periods      'sum' 'max'...
Calculation across locations    'sum' 'max'....
Means of Verification           Reportable.means_of_verification
Indicator Results level         ???
Indicator Location Name         IndicatorLocationData.location.name
Indicator Location Geo          IndicatorLocationData.location.point
Admin level of location         IndicatorLocationData.location.type.admin_level
Frequency                       IndicatorReport.frequency (Reportable, ProgrammeDocument ??)
Overall Status                  ProgressReport.review_overall_status
Narrative Assessment            IndicatorReport.narrative_assessment
Due date                        IndicatorReport.due_date
Submission date                 IndicatorReport.submission_date
Project activity                (cannot find this field maybe PartnerActivity?)

Totalbudget(ideally at most granular level tied to activity / result)
Utilised budget(same conditions as above)
Report  #
"""
from django.contrib.postgres.fields import JSONField
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

from redis.exceptions import LockError
from strategy_field.utils import get_attr

from etools_datamart.apps.etl.exceptions import MaxRecordsException, RequiredIsMissing, RequiredIsRunning
from etools_datamart.apps.etl.loader import BaseLoader, EtlResult, logger, RUN_UNKNOWN
from etools_datamart.apps.sources.source_prp.models import (CoreCountry, CoreGatewaytype,
                                                            IndicatorIndicatorlocationdata, IndicatorIndicatorreport,
                                                            IndicatorReportable, IndicatorReportablelocationgoal,
                                                            UnicefLowerleveloutput, UnicefPdresultlink,
                                                            UnicefProgrammedocument, UnicefProgressreport,)
from etools_datamart.sentry import process_exception

from .base import PrpDataMartModel


class PrpBaseLoader(BaseLoader):

    def get_queryset(self):
        if self.config.queryset:
            ret = self.config.queryset()
        elif self.config.source:
            ret = self.config.source.objects.all()
        else:  # pragma: no cover
            raise ValueError("Option must define 'queryset' or 'source' attribute")

        return ret

    def filter_queryset(self, qs):
        use_delta = self.context['only_delta'] and not self.context['is_empty']
        if self.config.filters:
            qs = qs.filter(**self.config.filters)
        if use_delta and (self.config.last_modify_field and self.last_run):
            logger.debug(f"Loader {self}: use deltas")
            qs = qs.filter(**{f"{self.config.last_modify_field}__gte": self.last_run})
        return qs

    def load(self, *, verbosity=0, stdout=None,
             ignore_dependencies=False, max_records=None,
             only_delta=True, run_type=RUN_UNKNOWN, **kwargs):
        self.on_start(run_type)
        self.results = EtlResult()
        logger.debug(f"Running loader {self}")
        lock = self.lock()
        truncate = self.config.truncate
        try:
            if lock:  # pragma: no branch
                if not ignore_dependencies:
                    for requirement in self.config.depends:
                        if requirement.loader.is_running():
                            raise RequiredIsRunning(requirement)
                        if requirement.loader.need_refresh(self):
                            raise RequiredIsMissing(requirement)
                        else:
                            logger.info(f"Loader {requirement} is uptodate")
                self.mapping = {}
                mart_fields = self.model._meta.concrete_fields
                for field in mart_fields:
                    if field.name not in ['source_id', 'id', 'last_modify_date']:
                        self.mapping[field.name] = field.name
                if self.config.mapping:  # pragma: no branch
                    self.mapping.update(self.config.mapping)
                self.update_context(today=timezone.now(),
                                    max_records=max_records,
                                    verbosity=verbosity,
                                    records=0,
                                    only_delta=only_delta,
                                    is_empty=not self.model.objects.exists(),
                                    stdout=stdout)
                sid = transaction.savepoint()
                try:
                    self.results.context = self.context
                    self.fields_to_compare = [f for f in self.mapping.keys() if f not in ["seen"]]
                    if truncate:
                        self.model.objects.truncate()
                    qs = self.filter_queryset(self.get_queryset())
                    for record in qs.all():
                        filters = self.config.key(self, record)
                        values = self.get_values(record)
                        op = self.process_record(filters, values)
                        self.increment_counter(op)

                    if stdout and verbosity > 0:
                        stdout.write("\n")
                    # deleted = self.model.objects.exclude(seen=today).delete()[0]
                    # self.results.deleted = deleted
                except MaxRecordsException:
                    pass
                except Exception:
                    transaction.savepoint_rollback(sid)
                    raise
            else:
                logger.info(f"Unable to get lock for {self}")

        except (RequiredIsMissing, RequiredIsRunning) as e:
            self.on_end(error=e, retry=True)
            raise
        except BaseException as e:
            self.on_end(e)
            process_exception(e)
            raise
        else:
            self.on_end(None)
        finally:
            if lock:  # pragma: no branch
                try:
                    lock.release()
                except LockError as e:  # pragma: no cover
                    logger.warning(e)

        return self.results


class IndicatorByLocationLoader(PrpBaseLoader):
    def get_location_levelname(self, record, values, field_name):
        pass

    def get_country(self, record, values, field_name):
        try:
            gw = CoreGatewaytype.objects.get(id=record.location.gateway_id)
            values['location_levelname'] = gw.name
            return CoreCountry.objects.get(id=gw.country_id).name
        except Exception:
            return None


class IndicatorByLocation(PrpDataMartModel):
    country = models.CharField(max_length=100, blank=True, null=True)
    project = models.CharField(max_length=255, blank=True, null=True)
    partner = models.CharField(max_length=255, blank=True, null=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    indicator_target = models.CharField(max_length=50, blank=True, null=True)
    indicator_baseline = models.CharField(max_length=50, blank=True, null=True)
    title_of_indicator = models.TextField(max_length=2048, blank=True, null=True)

    location_source_id = models.IntegerField(blank=True, null=True)
    location_name = models.CharField(max_length=254, blank=True, null=True)
    location_pcode = models.CharField(max_length=32, blank=True, null=True)
    location_level = models.IntegerField(blank=True, null=True)
    location_levelname = models.CharField(max_length=32, blank=True, null=True)

    loader = IndicatorByLocationLoader()

    class Meta:
        app_label = 'prp'

    class Options:
        queryset = IndicatorIndicatorlocationdata.objects.select_related('location',
                                                                         # 'indicator_report__project__partner',
                                                                         # 'indicator_report__progress_report__programme_document',
                                                                         # 'indicator_report__reportable'
                                                                         ).all
        source = IndicatorIndicatorlocationdata
        key = lambda loader, record: {'source_id': record.id}
        mapping = {
            'location_source_id': 'location.id',
            'location_name': 'location.title',
            'location_pcode': 'location.p_code',
            'location_level': 'location.level',
            'location_levelname': 'i',
            'country': '-',
            'project': 'indicator_report.project.title',
            'partner': 'indicator_report.project.partner.title',
            'reference_number': 'indicator_report.progress_report.programme_document.reference_number',
            'indicator_baseline': 'indicator_report.reportable.baseline',
            'indicator_target': 'indicator_report.reportable.target',
            'title_of_indicator': 'indicator_report.title'
        }


class DataReportLoader(PrpBaseLoader):

    def get_queryset(self):
        # all_progress_reports = UnicefProgressreport.objects.all()
        qs = IndicatorIndicatorlocationdata.objects.all()
        qs = qs.exclude(Q(indicator_report__progress_report__isnull=True) |
                        Q(indicator_report__progress_report__status__in=["Due",
                                                                         "Ove",
                                                                         "Sen"]))
        return qs.all()

    def get_value(self, field_name, value_or_func, original_record, current_mapping):
        return super().get_value(field_name, value_or_func, original_record, current_mapping)

    def get_values(self, record: IndicatorIndicatorlocationdata):
        record._reportable: IndicatorReportable = record.indicator_report.reportable
        return super().get_values(record)

    def process_record(self, filters, values):
        return super().process_record(filters, values)

    def get_cp_output_indicators(self, record: IndicatorIndicatorlocationdata, values, **kwargs):
        return 'N/A'

    def get_etools_cp_output_indicators_id(self, record: IndicatorIndicatorlocationdata, values, **kwargs):
        return 'N/A'

    def get_locations(self, record: IndicatorIndicatorlocationdata, values, **kwargs):
        # PartnersInterventionFlatLocations
        locs = []
        # intervention: PartnersIntervention = original.activity.intervention
        # for location in original.activity.locations.select_related('gateway').order_by('id'):
        qs = (IndicatorReportablelocationgoal.objects
              .select_related('location')
              .filter(reportable=record.indicator_report.reportable))
        for entry in qs.all():
            location = entry.location
            locs.append(dict(
                source_id=location.id,
                name=location.title,
                pcode=location.p_code,
                level=location.level,
                levelname=location.gateway.name
            ))
        values['locations_data'] = locs
        return ", ".join([l['name'] for l in locs])

    def get_submitted_by(self, record: IndicatorIndicatorlocationdata, values, **kwargs):
        user = get_attr(record, 'indicator_report.progress_report.submitted_by')
        if user:
            return "%s %s (%s)" % (user.first_name, user.last_name, user.email)

    def get_programme_document(self, record: IndicatorIndicatorlocationdata, values, **kwargs):
        # UnicefLowerleveloutput.
        # r: IndicatorReportable = record.indicator_report.reportable
        ct = record._reportable.content_type
        if ct.model == 'lowerleveloutput':
            ll: UnicefLowerleveloutput = UnicefLowerleveloutput.objects.get(id=record._reportable.object_id)
            cp_output: UnicefPdresultlink = ll.cp_output
            values['cp_output'] = cp_output.title
            values['etools_cp_output_id'] = cp_output.external_cp_output_id

            record._programme_document = cp_output.programme_document
            record.indicator_report.reportable.lower_level_output = ll
            return cp_output.programme_document.title
        return None

    def get_total_cumulative_progress(self, record: IndicatorIndicatorlocationdata, values, **kwargs):
        return record._reportable.total["c"]

    def get_progress_report(self, record: IndicatorIndicatorlocationdata, values, **kwargs):
        ir: IndicatorIndicatorreport = record.indicator_report
        pr: UnicefProgressreport = ir.progress_report
        if pr:
            pd: UnicefProgrammedocument = pr.programme_document
            return "Progress Report <pk:{}>: {} {} to {}".format(
                pr.id, pd.title, pr.start_date, pr.end_date
            )


class DataReport(PrpDataMartModel):
    # | indicator_report | idl.indicator_report |
    indicator_report = models.CharField(max_length=2048, blank=True, null=True)
    # | progres_report | indicator_report.progres_report |
    progress_report = models.CharField(max_length=2048, blank=True, null=True)
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
    # | means_of_verification | r.means_of_verification |
    means_of_verification = models.CharField(max_length=2048, blank=True, null=True)
    # | locations | r.lower_level_output.locations.all()  # magic by stefano|
    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True)
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
    # | face_attachment | "nope" |
    # | attachment_1 | "nope" |
    # | attachment_2 | "nope" |
    # | narrative | progres_report.narrative |
    narrative = models.CharField(max_length=2048, blank=True, null=True)
    # | pd_output_progress_status | indicator_report.overall_status |
    pd_output_progress_status = models.CharField(max_length=2048, blank=True, null=True)
    # | pd_output_narrative_assessment | indicator_report.narrative_assessment |
    pd_output_narrative_assessment = models.CharField(max_length=2048, blank=True, null=True)
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
    loader = DataReportLoader()

    class Meta:
        app_label = 'prp'

    class Options:
        key = lambda loader, record: {'source_id': record.id}
        mapping = {'indicator_report': 'indicator_report.title',
                   'progress_report': 'indicator_report.progress_report',
                   # 'programme_document': 'indicator_report.reportable.lower_level_output.cp_output.programme_document',
                   'programme_document': '-',
                   'country_name': '_programme_document.workspace.title',
                   'business_area': '_programme_document.workspace.business_area_code',
                   'partner_name': '_programme_document.partner.title',
                   'partner_vendor_number': '_programme_document.partner.vendor_number',
                   'etools_intervention_id': '_programme_document.external_id',
                   'prp_intervention_id': '_programme_document.id',
                   'intervention_reference_number': '_programme_document.reference_number',
                   'cp_output': 'i',
                   'etools_cp_output_id': 'i',
                   'pd_result': 'indicator_report.reportable.lower_level_output.title',
                   'etools_pd_result_id': 'indicator_report.reportable.lower_level_output.external_id',
                   'performance_indicator': 'indicator_report.reportable.blueprint.title',
                   'section': 'N/A',
                   'cluster_indicator': 'indicator_report.reportable.is_cluster_indicator',
                   'indicator_type': 'indicator_report.reportable.blueprint.display_type',
                   'baseline': 'indicator_report.reportable.calculated_baseline',
                   'target': 'indicator_report.reportable.calculated_target',
                   'high_frequency': 'indicator_report.reportable.is_unicef_hf_indicator',
                   'means_of_verification': 'indicator_report.reportable.means_of_verification',
                   'locations': '-',
                   'locations_data': 'i',
                   'report_number': 'indicator_report.progress_report.report_number',
                   'due_date': 'indicator_report.progress_report.due_date',
                   'reporting_period_start_date': 'indicator_report.progress_report.start_date',
                   'reporting_period_end_date': 'indicator_report.progress_report.end_date',
                   'reporting_period_due_date': 'indicator_report.progress_report.due_date',
                   'report_submission_date': 'indicator_report.progress_report.submission_date',
                   'submitted_by': '-',
                   'narrative': 'indicator_report.progress_report.narrative',
                   'pd_output_progress_status': 'indicator_report.overall_status',
                   'pd_output_narrative_assessment': 'indicator_report.narrative_assessment',
                   'calculation_method_across_location': 'indicator_report.reportable.blueprint.calculation_formula_across_locations',
                   'calculation_method_across_reporting_periods': 'indicator_report.reportable.blueprint.calculation_formula_across_periods',
                   'current_location': 'location.title',
                   'previous_location_progress': 'previous_location_data.title',
                   'total_cumulative_progress_in_location': 'N/A',
                   'total_cumulative_progress': '-'
                   }
