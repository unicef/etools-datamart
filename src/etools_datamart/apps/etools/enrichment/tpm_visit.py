from django.db import models

from etools_datamart.apps.etools.enrichment.utils import create_alias
from etools_datamart.apps.etools.models import (TpmpartnersTpmpartnerstaffmember, TpmTpmvisit,
                                                TpmTpmvisitTpmPartnerFocalPoints,)

models.ManyToManyField(TpmpartnersTpmpartnerstaffmember,
                       through=TpmTpmvisitTpmPartnerFocalPoints,
                       ).contribute_to_class(TpmTpmvisit, 'tpm_partner_focal_points')

aliases = (['tpmtpmvisit_tpm_tpmactivity_tpm_visit_id', 'tpm_activities'],)
create_alias(TpmTpmvisit, aliases)


def get_reference_number(self, country):
    return '{}/{}/{}/TPM'.format(
        country.country_short_code or '',
        self.created.year,
        self.id,
    )


TpmTpmvisit.get_reference_number = get_reference_number
