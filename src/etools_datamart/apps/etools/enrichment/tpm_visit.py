from django.db import models

from etools_datamart.apps.etools.enrichment.utils import create_alias
from etools_datamart.apps.etools.models import (TpmpartnersTpmpartnerstaffmember, TpmTpmvisit,
                                                TpmTpmvisitTpmPartnerFocalPoints,)

models.ManyToManyField(TpmpartnersTpmpartnerstaffmember,
                       through=TpmTpmvisitTpmPartnerFocalPoints,
                       ).contribute_to_class(TpmTpmvisit, 'tpm_partner_focal_points')

aliases = (['tpmtpmvisit_tpm_tpmactivity_tpm_visit_id', 'tpm_activities'], )
create_alias(TpmTpmvisit, aliases)
