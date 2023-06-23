from django.db import models

from etools_datamart.apps.sources.etools.models import (
    AuthUser,
    TpmTpmactivity,
    TpmTpmvisit,
    TpmTpmvisitTpmPartnerFocalPoints,
)

from .utils import create_alias

models.ManyToManyField(
    AuthUser,
    through=TpmTpmvisitTpmPartnerFocalPoints,
).contribute_to_class(TpmTpmvisit, "tpm_partner_focal_points")

aliases = (["tpmtpmvisit_tpm_tpmactivity_tpm_visit_id", "tpm_activities"],)
create_alias(TpmTpmvisit, aliases)


def get_reference_number(self, country):
    return "{}/{}/{}/TPM".format(
        country.country_short_code or "",
        self.created.year,
        self.id,
    )


def _get_reference_number(self):
    return "{}/{}/{}/TPM".format(
        self.get_country_instance().country_short_code or "",
        self.created.year,
        self.id,
    )


def _get_activities(self):
    return TpmTpmactivity.objects.filter(tpm_visit=self)


def _get_start_date(self):
    return self.activities.aggregate(date__min=models.Max("activity_ptr__date"))["date__min"]


def _get_end_date(self):
    return self.activities.aggregate(date__max=models.Max("activity_ptr__date"))["date__max"]


# TpmTpmvisit.get_reference_number = get_reference_number
TpmTpmvisit.reference_number = property(_get_reference_number)
TpmTpmvisit.activities = property(_get_activities)
TpmTpmvisit.start_date = property(_get_start_date)
TpmTpmvisit.end_date = property(_get_end_date)
