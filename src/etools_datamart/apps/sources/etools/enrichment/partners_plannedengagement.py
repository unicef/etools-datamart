from django.db import models

from etools_datamart.apps.sources.etools.models import PartnersPartnerorganization, PartnersPlannedengagement

f = [f for f in PartnersPlannedengagement._meta.local_fields if f.name != "partner"]
PartnersPlannedengagement._meta.local_fields = f


def required_audit(self):
    return sum([self.scheduled_audit, self.special_audit])


PartnersPlannedengagement.required_audit = property(required_audit)

models.OneToOneField(
    PartnersPartnerorganization, related_name="planned_engagement", on_delete=models.PROTECT
).contribute_to_class(PartnersPlannedengagement, "partner")
