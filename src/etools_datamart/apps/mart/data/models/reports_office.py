from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import ReportsOffice


class OfficeLoader(EtoolsLoader):
    def get_queryset(self):
        return ReportsOffice.objects.all()


class Office(EtoolsDataMartModel):
    name = models.CharField(max_length=254, null=True, blank=True)

    loader = OfficeLoader()

    class Options:
        source = ReportsOffice
        # key = lambda loader, record: dict(
        #     schema_name=loader.context['country'].schema_name,
        #     source_id=record.pk,
        # )
