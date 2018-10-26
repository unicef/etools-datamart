from django.db import connections

from etools_datamart.apps.etools.models import UsersUserprofile


def get_etools_allowed_schemas(user):
    # returns all allowed schemas as per eTools configuration
    # if `user` is also an eTools user.
    # matching is performed per email mnatching

    conn = connections['etools']
    with conn.noschema():
        etools_user = UsersUserprofile.objects.filter(user__email=user.email).first()
        if etools_user:
            return set(etools_user.countries_available.values_list('schema_name', flat=True))
        else:
            return set()
