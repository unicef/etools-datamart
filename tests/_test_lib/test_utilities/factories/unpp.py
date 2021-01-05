from test_utilities.factories import RegisterModelFactory

from etools_datamart.apps.mart.unpp import models


class LocationMartModelFactory(RegisterModelFactory):
    class Meta:
        model = models.Location


class ApplicationMartModelFactory(RegisterModelFactory):
    class Meta:
        model = models.Application
