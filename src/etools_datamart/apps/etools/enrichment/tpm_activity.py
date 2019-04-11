from django.db import models

from etools_datamart.apps.etools.models import (ActivitiesActivity, ActivitiesActivityLocations, AuthUser,
                                                LocationsLocation, TpmTpmactivity, TpmTpmactivityUnicefFocalPoints,)

models.ManyToManyField(LocationsLocation,
                       through=ActivitiesActivityLocations,
                       ).contribute_to_class(ActivitiesActivity, 'locations')

models.ManyToManyField(AuthUser,
                       through=TpmTpmactivityUnicefFocalPoints,
                       ).contribute_to_class(TpmTpmactivity, 'unicef_focal_points')

pk = TpmTpmactivity._meta.get_field('activity_ptr')
TpmTpmactivity._meta.pk = pk
TpmTpmactivity._meta.auto_field = pk
