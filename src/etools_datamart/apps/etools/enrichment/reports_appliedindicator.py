from django.db import models

from etools_datamart.apps.etools.models import ReportsDisaggregation, ReportsAppliedindicatorDisaggregation, \
    ReportsAppliedindicator, LocationsLocation, ReportsAppliedindicatorLocations

models.ManyToManyField(ReportsDisaggregation,
                       through=ReportsAppliedindicatorDisaggregation,
                       ).contribute_to_class(ReportsAppliedindicator, 'disaggregations')

models.ManyToManyField(LocationsLocation,
                       through=ReportsAppliedindicatorLocations,
                       ).contribute_to_class(ReportsAppliedindicator, 'locations')
