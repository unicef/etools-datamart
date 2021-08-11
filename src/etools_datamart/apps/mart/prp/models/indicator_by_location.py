from django.db import models
from django.db.models import JSONField, Q

from etools_datamart.apps.mart.prp.base import PrpDataMartModel
from etools_datamart.apps.mart.prp.models.base import PrpBaseLoader
from etools_datamart.apps.sources.source_prp.models import CoreCountry, CoreGatewaytype, IndicatorIndicatorlocationdata


class IndicatorByLocationLoader(PrpBaseLoader):
    # def get_location_levelname(self, record, values, field_name):
    #     pass

    # def get_country(self, record, values, field_name):
    #     breakpoint()
    #     try:
    #         gw = CoreGatewaytype.objects.get(id=record.location.gateway_id)
    #         values['location_levelname'] = gw.name
    #         return CoreCountry.objects.get(id=gw.country_id).name
    #     except Exception:
    #         return None

    pass


class IndicatorByLocation(PrpDataMartModel):
    country = models.CharField(max_length=100, blank=True, null=True)
    project = models.CharField(max_length=255, blank=True, null=True)
    partner = models.CharField(max_length=255, blank=True, null=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    indicator_target = models.CharField(max_length=50, blank=True, null=True)
    indicator_baseline = models.CharField(max_length=50, blank=True, null=True)
    title_of_indicator = models.TextField(max_length=2048, blank=True, null=True)

    location_source_id = models.IntegerField(blank=True, null=True)
    location_name = models.CharField(max_length=254, blank=True, null=True)
    location_pcode = models.CharField(max_length=32, blank=True, null=True)
    location_level = models.IntegerField(blank=True, null=True)
    location_levelname = models.CharField(max_length=32, blank=True, null=True)

    loader = IndicatorByLocationLoader()

    class Meta:
        app_label = 'prp'

    class Options:
        queryset = IndicatorIndicatorlocationdata.objects.select_related(
            'location',
            'location__gateway',
            # 'indicator_report__project',
            'indicator_report__project__partner',
            # 'indicator_report__progress_report',
            'indicator_report__progress_report__programme_document__workspace',
            'indicator_report__reportable'
        )
        mapping = {
            'location_source_id': 'location.id',
            'location_name': 'location.title',
            'location_pcode': 'location.p_code',
            'location_level': 'location.level',
            'location_levelname': 'location.gateway.name',
            'country': 'indicator_report.progress_report.programme_document.workspace.title',
            'project': 'indicator_report.project.title',
            'partner': 'indicator_report.project.partner.title',
            'reference_number': 'indicator_report.progress_report.programme_document.reference_number',
            'indicator_baseline': 'indicator_report.reportable.baseline',
            'indicator_target': 'indicator_report.reportable.target',
            'title_of_indicator': 'indicator_report.title'
        }
