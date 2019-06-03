from django.db import models

from etools_datamart.apps.etools.enrichment.utils import add_m2m
from etools_datamart.apps.etools.models import (LocationsLocation, T2FTravel, T2FTravelactivity,
                                                T2FTravelactivityLocations, T2FTravelactivityTravels,)

models.ManyToManyField(LocationsLocation,
                       through=T2FTravelactivityLocations,
                       ).contribute_to_class(T2FTravelactivity, 'locations')

add_m2m(T2FTravelactivity, 'travels', T2FTravel, T2FTravelactivityTravels)
# models.ManyToManyField(T2FTravel,
#                        through=T2FTravelactivityTravels,
#                        ).contribute_to_class(T2FTravelactivity, 'travels')
