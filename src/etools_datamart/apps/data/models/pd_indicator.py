from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models import Intervention, Location
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import models, ReportsAppliedindicator


class PDIndicatorLoader(Loader):

    def process_country(self):
        country = self.context['country']
        qs = self.filter_queryset(self.get_queryset())
        for indicator in qs.all():
            for disaggregation in indicator.disaggregations.all():
                indicator.disaggregation = disaggregation
                for location in indicator.locations.all():
                    indicator.location = location
                    filters = self.config.key(country, indicator)
                    values = self.get_values(indicator)
                    op = self.process_record(filters, values)
                    self.increment_counter(op)


class PDIndicator(DataMartModel):
    context_code = models.CharField(max_length=50, blank=True, null=True)
    assumptions = models.TextField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    # indicator = models.ForeignKey('ReportsIndicatorblueprint', models.DO_NOTHING,
    #                               related_name='reportsindicatorblueprint_reports_appliedindicator_indicator_id',
    #                               blank=True, null=True)
    # lower_result = models.ForeignKey('ReportsLowerresult', models.DO_NOTHING,
    #                                  related_name='reportslowerresult_reports_appliedindicator_lower_result_id')
    means_of_verification = models.CharField(max_length=255, blank=True, null=True)
    cluster_indicator_id = models.IntegerField(blank=True, null=True)
    cluster_indicator_title = models.CharField(max_length=1024, blank=True, null=True)
    cluster_name = models.CharField(max_length=512, blank=True, null=True)
    # created = models.DateTimeField(blank=True, null=True)
    # modified = models.DateTimeField(blank=True, null=True)
    response_plan_name = models.CharField(max_length=1024, blank=True, null=True)
    # section = models.ForeignKey('ReportsSector', models.DO_NOTHING,
    #                             related_name='reportssector_reports_appliedindicator_section_id', blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    is_high_frequency = models.BooleanField(blank=True, null=True)

    denominator_label = models.CharField(max_length=256, blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    measurement_specifications = models.TextField(blank=True, null=True)
    numerator_label = models.CharField(max_length=256, blank=True, null=True)

    # target = models.TextField()  # This field type is a guess.
    target_denominator = models.IntegerField(blank=True, null=True)
    target_numerator = models.IntegerField(blank=True, null=True)

    # baseline = models.TextField(blank=True, null=True)  # This field type is a guess.
    baseline_denominator = models.IntegerField(blank=True, null=True)
    baseline_numerator = models.IntegerField(blank=True, null=True)

    # from lower_result
    lower_result_name = models.CharField(max_length=500, blank=True, null=True)
    result_link_intervention = models.IntegerField(blank=True, null=True)

    # from section
    section_name = models.CharField(max_length=45, blank=True, null=True)

    # from blueprint
    title = models.CharField(max_length=1024, blank=True, null=True)
    # description = models.CharField(max_length=3072, blank=True, null=True)
    # code = models.CharField(max_length=50, blank=True, null=True)
    # subdomain = models.CharField(max_length=255, blank=True, null=True)
    # disaggregatable = models.BooleanField()
    unit = models.CharField(max_length=10, blank=True, null=True)
    # calculation_formula_across_locations = models.CharField(max_length=10, blank=True, null=True)
    # calculation_formula_across_periods = models.CharField(max_length=10, blank=True, null=True)
    display_type = models.CharField(max_length=10, blank=True, null=True)

    # from disaggregation
    disaggregation_name = models.CharField(max_length=255)
    disaggregation_active = models.BooleanField(default=False)

    # from location
    location_name = models.CharField(max_length=254, blank=True, null=True)

    # internals
    location = models.ForeignKey(Location, blank=True, null=True,
                                 on_delete=models.SET_NULL)

    intervention = models.ForeignKey(Intervention, blank=True, null=True,
                                     on_delete=models.SET_NULL)

    # origin
    source_disaggregation_id = models.IntegerField(blank=True, null=True)
    source_location_id = models.IntegerField(blank=True, null=True)

    loader = PDIndicatorLoader()

    class Meta:
        unique_together = (('schema_name',
                            'source_id',
                            'source_location_id',
                            'source_disaggregation_id',
                            ),)

    class Options:
        source = ReportsAppliedindicator
        queryset = ReportsAppliedindicator.objects.select_related('indicator', 'section').all

        key = lambda country, record: dict(schema_name=country.schema_name,
                                           source_id=record.pk,
                                           source_location_id=record.location.pk,
                                           source_disaggregation_id=record.disaggregation.pk)

        mapping = {'title': 'indicator.title',
                   # 'description': 'indicator.description',
                   # 'code': 'indicator.code',
                   # 'subdomain': 'indicator.subdomain',
                   # 'disaggregatable': 'indicator.disaggregatable',
                   'unit': 'indicator.unit',
                   # 'calculation_formula_across_locations': 'indicator.calculation_formula_across_locations`',
                   # 'calculation_formula_across_periods': 'indicator.calculation_formula_across_periods`',

                   'target_denominator': lambda c, r: r.target['d'],
                   'target_numerator': lambda c, r: r.target['v'],
                   'baseline_denominator': lambda c, r: r.baseline['d'],
                   'baseline_numerator': lambda c, r: r.baseline['v'],

                   'display_type': 'indicator.display_type`',
                   'section_name': 'section.name',
                   'lower_result_name': 'lower_result.name',
                   'result_link_intervention': 'lower_result.result_link.intervention.pk',

                   'disaggregation_name': 'disaggregation.name',
                   'disaggregation_active': 'disaggregation.active',

                   'location_name': 'location.name',
                   'location': lambda *a: None,

                   'source_disaggregation_id': 'disaggregation.id',
                   'source_location_id': 'location.id',
                   }
