from django.db import models

from etools_datamart.apps.sources.etools.models import AuthUser, UsersCountry, UsersUserprofile

f = [f for f in UsersUserprofile._meta.local_fields if f.name != "user_id"]
UsersUserprofile._meta.local_fields = f
UsersUserprofile._meta.unique_together = []
models.OneToOneField(AuthUser, related_name="profile", on_delete=models.PROTECT).contribute_to_class(
    UsersUserprofile, "user"
)


def countries_available(self):
    return UsersCountry.objects.filter(
        UsersRealm_country__in=self.user.UsersRealm_user.filter(is_active=True)
    ).distinct()


UsersUserprofile.countries_available = property(countries_available)
