from django.db import models
from django.db.models import F, Q

from etools_datamart.apps.mart.prp.base import PrpDataMartModel
from etools_datamart.apps.mart.prp.models.base import PrpBaseLoader
from etools_datamart.apps.sources.source_prp.models import IndicatorIndicatorreport


class IndicatorReportLoader(PrpBaseLoader):

    def get_queryset(self):
        qs = IndicatorIndicatorreport.objects.exclude(
            Q(progress_report__isnull=True) | Q(progress_report__status__in=["Due", "Ove", "Sen"])
        ).annotate(
            business_area=F('progress_report__programme_document__workspace__business_area_code'),
            intervention_reference_number=F('progress_report__programme_document__reference_number'),
            partner=F('progress_report__programme_document__partner__title'),
            performance_indicator=F('reportable__blueprint__title'),
            report_type=F('progress_report__report_type'),
            report_number=F('progress_report__report_number'),
            target=F('reportable__target'),
            baseline=F('reportable__baseline'),
            unit=F('reportable__blueprint__unit'),
            total_cumulative_progress=F('reportable__total'),
            pd_output_progress_status=F('overall_status'),
        )
        return qs


class IndicatorReport(PrpDataMartModel):

    business_area = models.CharField(max_length=2048, blank=True, null=True)
    partner = models.CharField(max_length=255, blank=True, null=True)
    report_type = models.CharField(max_length=3, blank=True, null=True)
    report_number = models.IntegerField(blank=True, null=True)
    intervention_reference_number = models.CharField(max_length=2048, blank=True, null=True)
    pd_output_progress_status = models.CharField(max_length=2048, blank=True, null=True)
    performance_indicator = models.CharField(max_length=2048, blank=True, null=True)
    baseline = models.CharField(max_length=2048, blank=True, null=True)
    target = models.CharField(max_length=2048, blank=True, null=True)
    unit = models.CharField(max_length=10, blank=True, null=True)
    total_cumulative_progress = models.CharField(max_length=2048, blank=True, null=True)
    time_period_start = models.DateField(blank=True, null=True)
    time_period_end = models.DateField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    loader = IndicatorReportLoader()

    class Meta:
        app_label = 'prp'

    def __str__(self):
        return f'{self.business_area} | {self.intervention_reference_number} | {self.pd_output_progress_status}'

    class Options:
        mapping = {}
