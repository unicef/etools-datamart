from django.contrib.postgres.fields import JSONField
from django.db import models

from etools_datamart.apps.data.fields import SafeDecimal
from etools_datamart.apps.data.loader import EtoolsLoader
from etools_datamart.apps.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.data.models.mixins import NestedLocationLoaderMixin, NestedLocationMixin
from etools_datamart.apps.etools.models import PartnersIntervention, ReportsAppliedindicator, ReportsLowerresult


def get_pd_output_names(obj: PartnersIntervention):
    return [ll.name for rl in obj.result_links.all() for ll in rl.ll_results.all()]


class ReportIndicatorLoader(NestedLocationMixin, EtoolsLoader):
    location_m2m_field = 'locations'

    def get_baseline_denominator(self, record, values, field_name):
        value = SafeDecimal(record.baseline.get('d'))
        if value:
            value._validate_for_field(ReportIndicator._meta.get_field(field_name))
        return value

    def get_baseline_numerator(self, record, values, field_name):
        value = SafeDecimal(record.baseline.get('v'))
        if value:
            value._validate_for_field(ReportIndicator._meta.get_field(field_name))
        return value

    def get_target_value(self, record, values, field_name):
        values['target_denominator'] = SafeDecimal(record.target.get('d'))
        values['target_numerator'] = SafeDecimal(record.target.get('v'))

    def get_disaggregations(self, record, values, field_name):
        ret = []
        for disaggregatio in record.disaggregations.order_by('id'):
            ret.append(dict(
                source_id=disaggregatio.id,
                name=disaggregatio.name,
                active=disaggregatio.active
            ))
        values['disaggregations_data'] = ret
        return ", ".join([l['name'] for l in ret])

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
        ll_results = (ReportsLowerresult
                      .objects
                      .filter(result_link=record.lower_result.result_link)
                      .order_by('modified'))
        ret = []
        for pd_output in ll_results.all():
            ret.append(dict(last_modify_date=str(pd_output.modified),
                            name=pd_output.name,
                            ))
        values['pd_outputs_data'] = ret
        return ", ".join([l['name'] for l in ret])

    def process_country(self):
        qs = self.filter_queryset(self.get_queryset())
        for record in qs.all():
            filters = self.config.key(self, record)
            values = self.get_values(record)
            op = self.process_record(filters, values)
            self.increment_counter(op)


class ReportIndicator(NestedLocationLoaderMixin, EtoolsDataMartModel):
    assumptions = models.TextField(null=True, blank=True, )
    baseline = JSONField(default=dict, blank=True, null=True)
    baseline_denominator = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=3)
    baseline_numerator = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=3)
    # baseline_denominator = models.IntegerField(blank=True, null=True)
    # baseline_numerator = models.IntegerField(blank=True, null=True)
    cluster_indicator_id = models.PositiveIntegerField(blank=True, null=True, )
    cluster_indicator_title = models.CharField(max_length=1024, blank=True, null=True, )
    cluster_name = models.CharField(max_length=512, blank=True, null=True, )
    # code = models.CharField(max_length=50, blank=True, null=True)
    context_code = models.CharField(max_length=50, null=True, blank=True, )
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
    means_of_verification = models.CharField(max_length=255, null=True, blank=True, )
    measurement_specifications = models.TextField(max_length=4048, blank=True, null=True)
    numerator_label = models.CharField(max_length=256, blank=True, null=True)
    pd_outputs = models.TextField(blank=True, null=True)
    pd_outputs_data = JSONField(blank=True, null=True)
    # pd_output_indicator_last_modify_date = models.DateField(blank=True, null=True)
    pd_output_indicator_title = models.CharField(max_length=256, blank=True, null=True)
    # pd_output_name = models.CharField(max_length=256, blank=True, null=True)
    # pd_output_section = models.CharField(max_length=256, blank=True, null=True)
    pd_sffa_reference_number = models.CharField(max_length=256, blank=True, null=True)
    response_plan_name = models.CharField(max_length=1024, blank=True, null=True, )
    result_link_intervention = models.IntegerField(blank=True, null=True)
    section_name = models.CharField(max_length=45, blank=True, null=True)
    # source_disaggregation_id = models.IntegerField(blank=True, null=True)
    # source_location_id = models.IntegerField(blank=True, null=True)
    target = JSONField(default=dict, blank=True, null=True)
    target_denominator = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=3)
    target_numerator = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=3)
    # target_denominator = models.IntegerField(blank=True, null=True)
    # target_numerator = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    total = models.IntegerField(null=True, blank=True, default=0, )
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
        mapping = dict(
            baseline_denominator='-',
            baseline_numerator='-',
            cluster_indicator_id="=",
            cluster_indicator_title="=",
            cluster_name="=",
            cp_output_name="lower_result.result_link.cp_output.name",
            cp_output_type="lower_result.result_link.cp_output.result_type.name",
            denominator_label="=",
            disaggregations='-',
            disaggregations_data='i',
            # disaggregation_active='disaggregation.active',
            # disaggregation_name='disaggregation.name',
            display_type='indicator.display_type',
            is_active="=",
            is_high_frequency="=",
            label="=",
            locations='-',
            # locations_data='i',
            lower_result_name='lower_result.name',
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
            result_link_intervention='lower_result.result_link.intervention.pk',
            section_name='section.name',
            # source_disaggregation_id='disaggregation.id',
            # source_location_id='location.id',
            # target_denominator=lambda loader, record: record.target['d'],
            # target_numerator=lambda loader, record: record.target['v'],
            target_denominator='get_target_value',
            target_numerator='get_target_value',
            title='indicator.title',
            unit='indicator.unit',
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
