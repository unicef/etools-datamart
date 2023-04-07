from django.db import models

from etools_datamart.apps.sources.etools.models import (
    ActivitiesActivity,
    ActivitiesActivityLocations,
    AuthUser,
    LocationsLocation,
    ReportsOffice,
    TpmTpmactivity,
    TpmTpmactivityOffices,
    TpmTpmactivityUnicefFocalPoints,
)

from .utils import set_primary_key

models.ManyToManyField(
    LocationsLocation,
    through=ActivitiesActivityLocations,
).contribute_to_class(ActivitiesActivity, "locations")

models.ManyToManyField(
    AuthUser,
    through=TpmTpmactivityUnicefFocalPoints,
).contribute_to_class(TpmTpmactivity, "unicef_focal_points")

models.ManyToManyField(
    ReportsOffice,
    through=TpmTpmactivityOffices,
).contribute_to_class(TpmTpmactivity, "offices")


# pk = TpmTpmactivity._meta.get_field('activity_ptr')
# TpmTpmactivity._meta.pk = pk
# TpmTpmactivity._meta.auto_field = pk


def get_reference_number(self):
    return self.tpm_visit.reference_number


# TpmTpmactivity.id = property(lambda self: self.activity_ptr_id)
# TpmTpmactivity.pk = property(lambda self: self.activity_ptr_id)

TpmTpmactivity.reference_number = property(get_reference_number)
# TpmTpmactivity.activity = property(lambda self: self.activity_ptr)

set_primary_key(TpmTpmactivity, "activity_ptr")

TpmTpmactivity.task_number = property(
    lambda self: list(self.tpm_visit.tpm_activities.values_list("id", flat=True)).index(self.id) + 1
)


def fix_related_names(model, names):
    for field_name, related_name in names:
        field = model._meta.get_field(field_name)
        # field.remote_field.related_query_name = related_name
        related_model = field.remote_field.model
        old_reverse = getattr(related_model, field.related_query_name())
        setattr(related_model, related_name, old_reverse)
        assert getattr(related_model(), related_name)


related = (["tpm_visit", "activities"],)

fix_related_names(TpmTpmactivity, related)
