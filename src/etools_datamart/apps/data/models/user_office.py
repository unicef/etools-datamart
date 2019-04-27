from django.db import models

from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import UsersOffice


class Office(DataMartModel):
    name = models.CharField(max_length=254, blank=True, null=True)
    zonal_chief_email = models.CharField(max_length=254, blank=True, null=True)

    zonal_chief_source_id = models.IntegerField(blank=True, null=True)

    class Meta:
        pass

    class Options:
        source = UsersOffice
        # truncate = True
        # sync_deleted_records = lambda loader: False

        key = lambda loader, record: dict(country_name=loader.context['country'].name,
                                          schema_name=loader.context['country'].schema_name,
                                          source_id=record.id)
        mapping = {'zonal_chief_email': 'zonal_chief.email',
                   'zonal_chief_source_id': 'zonal_chief.id'
                   }
