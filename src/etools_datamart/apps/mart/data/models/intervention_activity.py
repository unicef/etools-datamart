from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Intervention
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention_epd import InterventionSimpleAbstract
from etools_datamart.apps.sources.etools.models import ReportsInterventionactivityitem


class InterventionActivityLoader(EtoolsLoader):
    pass


class InterventionActivity(InterventionSimpleAbstract, EtoolsDataMartModel):
    name = models.CharField(max_length=150, null=True, blank=True)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    cso_cash = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    no_units = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=150, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    code = models.CharField(max_length=50, blank=True, null=True)

    activity = models.CharField(max_length=150, blank=True, null=True)
    activity_details = models.TextField(blank=True, null=True)
    activity_unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    activity_cso_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    activity_code = models.CharField(max_length=50, blank=True, null=True)

    # LL
    ll_name = models.CharField(max_length=500, blank=True, null=True)
    ll_code = models.CharField(max_length=50, blank=True, null=True)

    loader = InterventionActivityLoader()

    class Meta:
        verbose_name = "Intervention Activity"

    class Options:
        source = ReportsInterventionactivityitem
        depends = (Intervention,)
        mapping = dict()
        queryset = lambda: ReportsInterventionactivityitem.objects.select_related(
            'activity__result__result_link__intervention__agreement__partner'
        )

    # ReportsInterventionactivity ** LL, CP, INT, PART
    # ReportsInterventionactivityTimeFrames **
    # ReportsInterventionactivityitem
    # ReportsInterventiontimeframe