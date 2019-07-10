from django.db import models

from etools_datamart.apps.etools.enrichment.utils import set_primary_key
from etools_datamart.apps.etools.models import (ActivitiesActivity, ActivitiesActivityLocations, AuthUser,
                                                LocationsLocation, TpmTpmactivity, TpmTpmactivityOffices,
                                                TpmTpmactivityUnicefFocalPoints, UsersOffice,)

models.ManyToManyField(LocationsLocation,
                       through=ActivitiesActivityLocations,
                       ).contribute_to_class(ActivitiesActivity, 'locations')

models.ManyToManyField(AuthUser,
                       through=TpmTpmactivityUnicefFocalPoints,
                       ).contribute_to_class(TpmTpmactivity, 'unicef_focal_points')

models.ManyToManyField(UsersOffice,
                       through=TpmTpmactivityOffices,
                       ).contribute_to_class(TpmTpmactivity, 'offices')


pk = TpmTpmactivity._meta.get_field('activity_ptr')
TpmTpmactivity._meta.pk = pk
TpmTpmactivity._meta.auto_field = pk


def get_reference_number(self):
    return self.tpm_visit.reference_number


TpmTpmactivity.reference_number = property(get_reference_number)
TpmTpmactivity.activity = property(lambda self: self.activity_ptr)

set_primary_key(TpmTpmactivity, 'activity_ptr')

TpmTpmactivity.task_number = property(lambda self:
                                      list(self.tpm_visit.tpm_activities.values_list('id', flat=True)).index(
                                          self.id) + 1)
