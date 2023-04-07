from django.db import models

from etools_datamart.apps.sources.etools.models import (
    LocationsLocation,
    ReportsAppliedindicator,
    ReportsAppliedindicatorDisaggregation,
    ReportsAppliedindicatorLocations,
    ReportsDisaggregation,
)

models.ManyToManyField(
    ReportsDisaggregation,
    through=ReportsAppliedindicatorDisaggregation,
).contribute_to_class(ReportsAppliedindicator, "disaggregations")

models.ManyToManyField(
    LocationsLocation,
    through=ReportsAppliedindicatorLocations,
).contribute_to_class(ReportsAppliedindicator, "locations")
