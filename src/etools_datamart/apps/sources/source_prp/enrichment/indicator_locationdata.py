from etools_datamart.apps.sources.source_prp.models import IndicatorIndicatorlocationdata, IndicatorIndicatorreport


def get_previous_location_data(self: IndicatorIndicatorlocationdata):
    previous_indicator_reports = (IndicatorIndicatorreport.objects
                                  .exclude(id=self.indicator_report.id)
                                  .filter(time_period_start__lt=self.indicator_report.time_period_start)
                                  )

    # previous_indicator_reports = self.indicator_report.reportable.indicator_reports.exclude(
    #     id=self.indicator_report.id
    # ).filter(time_period_start__lt=self.indicator_report.time_period_start)

    previous_report = previous_indicator_reports.order_by('-time_period_start').first()
    if previous_report:
        return previous_report.IndicatorIndicatorlocationdata_indicator_report.filter(location=self.location).first()


IndicatorIndicatorlocationdata.previous_location_data = property(get_previous_location_data)
