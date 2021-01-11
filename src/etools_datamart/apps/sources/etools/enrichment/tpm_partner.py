from django.db import models

from etools_datamart.apps.sources.etools.models import (
    TpmpartnersTpmpartner,
    TpmpartnersTpmpartnerCountries,
    UsersCountry,
)

models.ManyToManyField(UsersCountry,
                       through=TpmpartnersTpmpartnerCountries,
                       ).contribute_to_class(TpmpartnersTpmpartner, 'countries')
