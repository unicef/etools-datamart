from django.db import models

from etools_datamart.apps.sources.etools.models import AuthUser, AuthUserOldGroups

f = [f for f in AuthUserOldGroups._meta.local_fields if f.name != "user_id"]
AuthUserOldGroups._meta.local_fields = f
AuthUserOldGroups._meta.unique_together = []

models.OneToOneField(AuthUser, on_delete=models.PROTECT).contribute_to_class(AuthUserOldGroups, "user")
