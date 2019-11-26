from django.db import models

from etools_datamart.apps.sources.etools.models import AuthUser, AuthUserGroups

f = [f for f in AuthUserGroups._meta.local_fields if f.name != 'user_id']
AuthUserGroups._meta.local_fields = f
AuthUserGroups._meta.unique_together = []

models.OneToOneField(AuthUser,
                     on_delete=models.PROTECT).contribute_to_class(AuthUserGroups, 'user')
