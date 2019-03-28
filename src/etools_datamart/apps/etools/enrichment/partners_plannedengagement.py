from django.db import models

from etools_datamart.apps.etools.models import PartnersPlannedengagement, PartnersPartnerorganization

f = [f for f in PartnersPlannedengagement._meta.local_fields if f.name != 'partner']
PartnersPlannedengagement._meta.local_fields = f
models.OneToOneField(PartnersPartnerorganization,
                     related_name='planned_engagement',
                     on_delete=models.PROTECT).contribute_to_class(PartnersPlannedengagement,
                                                                   'partner')
