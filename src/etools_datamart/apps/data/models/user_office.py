from django.contrib.postgres.fields import JSONField
from django.db import models

from etools_datamart.apps.data.loader import EtoolsLoader
from etools_datamart.apps.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.etools.models import UsersCountryOffices, UsersOffice


class OfficeLoader(EtoolsLoader):
    def get_countries(self, record, values, **kwargs):
        ret = []
        for entry in UsersCountryOffices.objects.filter(office=record):
            ret.append({'name': entry.country.name,
                        'short_code': entry.country.country_short_code,
                        'area_code': entry.country.business_area_code,
                        'source_id': entry.country.id
                        })
        values['countries_data'] = ret
        return ", ".join([o['name'] for o in ret])


class Office(EtoolsDataMartModel):
    name = models.CharField(max_length=254, blank=True, null=True)
    zonal_chief_email = models.CharField(max_length=254, blank=True, null=True)
    countries = models.TextField(blank=True, null=True)
    countries_data = JSONField(blank=True, null=True, default=dict)

    zonal_chief_source_id = models.IntegerField(blank=True, null=True)

    loader = OfficeLoader()

    class Meta:
        pass

    class Options:
        source = UsersOffice
        # truncate = True
        # sync_deleted_records = lambda loader: False

        key = lambda loader, record: dict(schema_name=loader.context['country'].schema_name,
                                          source_id=record.id)
        mapping = {'zonal_chief_email': 'zonal_chief.email',
                   'zonal_chief_source_id': 'zonal_chief.id',
                   'countries': '-',
                   'countries_data': '-',
                   }
