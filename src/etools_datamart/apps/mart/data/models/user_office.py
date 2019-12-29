from django.db import models

from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import UsersOffice


class Office(EtoolsDataMartModel):
    name = models.CharField(max_length=254, blank=True, null=True)
    zonal_chief_email = models.CharField(max_length=254, blank=True, null=True)

    zonal_chief_source_id = models.IntegerField(blank=True, null=True)

    class Meta:
        pass

    class Options:
        source = UsersOffice
        # truncate = True
        # sync_deleted_records = lambda loader: False

        # key = lambda loader, record: dict(schema_name=loader.context['country'].schema_name,
        #                                   source_id=record.id)
        mapping = {'zonal_chief_email': 'zonal_chief.email',
                   'zonal_chief_source_id': 'zonal_chief.id'
                   }
