from django.db import models

from etools_datamart.apps.sources.etools.models import (
    AuthUser,
    UsersCountry,
    UsersUserprofile,
    UsersUserprofileCountriesAvailable,
)

f = [f for f in UsersUserprofile._meta.local_fields if f.name != 'user_id']
UsersUserprofile._meta.local_fields = f
UsersUserprofile._meta.unique_together = []
models.OneToOneField(AuthUser,
                     related_name='profile',
                     on_delete=models.PROTECT).contribute_to_class(UsersUserprofile, 'user')


# Fix UsersUserprofile ManyToManyField
models.ManyToManyField(UsersCountry,
                       through=UsersUserprofileCountriesAvailable,
                       ).contribute_to_class(UsersUserprofile, 'countries_available')
