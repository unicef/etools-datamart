from test_utilities.factories import RegisterModelFactory

from etools_datamart.apps.mart.prp import models


class DataReportMartModelFactory(RegisterModelFactory):
    class Meta:
        model = models.DataReport


class IndicatorReportMartModelFactory(RegisterModelFactory):
    class Meta:
        model = models.IndicatorReport
