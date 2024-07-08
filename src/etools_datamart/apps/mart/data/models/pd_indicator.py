from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import reverse

from celery.utils.log import get_task_logger

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.fields import SafeDecimal
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Location
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.mixins import add_location_mapping, LocationMixin
from etools_datamart.apps.sources.etools.models import models, ReportsAppliedindicator

logger = get_task_logger(__name__)


class PDIndicatorLoader(EtoolsLoader):
    def get_values(self, record):
        values = super().get_values(record)
        for k, v in values.items():
            if k in ["target_denominator", "target_numerator", "baseline_denominator", "baseline_numerator"]:
                values[k] = SafeDecimal(v)
                if values[k]:
                    values[k]._validate_for_field(PDIndicator._meta.get_field(k))

        return values

    def apply_locations(self, indicator):
        for location in indicator.locations.all():
            indicator.location = location
            filters = self.config.key(self, indicator)
            values = self.get_values(indicator)
            op = self.process_record(filters, values)
            self.increment_counter(op)

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = self.filter_queryset(self.get_queryset())

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for indicator in page.object_list:
                all_disaggregations = indicator.disaggregations.all()
                if 0 == len(all_disaggregations):
                    indicator.disaggregation = None
                    self.apply_locations(indicator)
                else:
                    for disaggregation in all_disaggregations:
                        indicator.disaggregation = disaggregation
                        self.apply_locations(indicator)

    def get_pd_url(self, record: ReportsAppliedindicator, values: dict, **kwargs):
        return reverse(
            "api:intervention-detail",
            args=["latest", record.lower_result.result_link.intervention.pk],
        )

    def get_disaggregation_name(self, record: ReportsAppliedindicator, values: dict, **kwargs):
        if record.disaggregation:
            return record.disaggregation.name
        return ""

    def get_disaggregation_active(self, record: ReportsAppliedindicator, values: dict, **kwargs):
        if record.disaggregation:
            return record.disaggregation.active
        return False


class PDIndicator(LocationMixin, EtoolsDataMartModel):
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
    pd_reference_number = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )

    # target = models.TextField()  # This field type is a guess.
    target_denominator = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=3)

    target_numerator = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=3)

    # baseline = models.TextField(blank=True, null=True)  # This field type is a guess.
    baseline_denominator = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    baseline_numerator = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)

    # from lower_result
    lower_result_name = models.CharField(max_length=500, blank=True, null=True)
    result_link_intervention = models.IntegerField(blank=True, null=True)
    pd_url = models.CharField(max_length=254, blank=True, null=True)

    # from section
    section_name = models.CharField(max_length=128, blank=True, null=True)

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

    # origin
    source_disaggregation_id = models.IntegerField(blank=True, null=True)
    source_location_id = models.IntegerField(blank=True, null=True)

    loader = PDIndicatorLoader()

    class Meta:
        unique_together = (
            (
                "schema_name",
                "source_id",
                "source_location_id",
                "source_disaggregation_id",
            ),
        )

    class Options:
        source = ReportsAppliedindicator
        queryset = ReportsAppliedindicator.objects.select_related
        (
            "indicator",
            "lower_result",
            "lower_result__result_link__intervention",
            "section",
        )

        key = lambda loader, record: dict(
            schema_name=loader.context["country"].schema_name,
            source_id=record.pk,
            source_location_id=record.location.pk,
            source_disaggregation_id=record.disaggregation.pk if record.disaggregation else None,
        )

        mapping = add_location_mapping(
            dict(
                title="indicator.title",
                unit="indicator.unit",
                target_denominator=lambda loader, record: record.target.get("d"),
                target_numerator=lambda loader, record: record.target.get("v"),
                baseline_denominator=lambda loader, record: record.baseline.get("d"),
                baseline_numerator=lambda loader, record: record.baseline.get("v"),
                display_type="indicator.display_type`",
                section_name="section.name",
                lower_result_name="lower_result.name",
                result_link_intervention="lower_result.result_link.intervention.pk",
                pd_reference_number="lower_result.result_link.intervention.reference_number",
                pd_url="-",
                disaggregation_name="-",
                disaggregation_active="-",
                location_name="location.name",
                location_pcode="location.p_code",
                location_level="location.admin_level",
                location_levelname="location.admin_level_name",
                location=lambda loader, record: Location.objects.filter(
                    source_id=record.id, schema_name=loader.context["country"].schema_name
                ).first(),
                source_disaggregation_id="disaggregation.id",
                source_location_id="location.id",
                # ----
                # baseline_denominator="N/A",
                # baseline_numerator="N/A",
                cluster_indicator_id="=",
                cluster_indicator_title="=",
                cluster_name="=",
                # cp_output="lower_result.result_link.cp_output.name",
                # cp_output_id="N/A",
                denominator_label="=",
                # disaggregation_active="N/A",
                # disaggregation_name="N/A",
                is_active="=",
                is_high_frequency="=",
                label="=",
                # location_level="N/A",
                # location_levelname="N/A",
                # location_name="N/A",
                # location_pcode="N/A",
                means_of_verification="=",
                measurement_specifications="=",
                numerator_label="=",
                # pd_output == lower_result.result_link.
                # pd_output_indicator_last_modify_date="N/A",
                # pd_output_indicator_title="N/A",
                # pd_output_name="N/A",
                # pd_output_section="N/A",
                # pd_sffa_reference_number="N/A",
                # response_plan_name="N/A",
                # source_disaggregation_id="N/A",
                # target_denominator="N/A",
                # target_numerator="N/A",
                # unit="N/A",
            )
        )
