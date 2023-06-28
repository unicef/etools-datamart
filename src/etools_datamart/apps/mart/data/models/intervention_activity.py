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
    unfunded_cash = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    no_units = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=150, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    code = models.CharField(max_length=50, blank=True, null=True)

    activity = models.CharField(max_length=150, blank=True, null=True)
    activity_details = models.TextField(blank=True, null=True)
    activity_unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    activity_cso_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    activity_unfunded_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
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
        mapping = dict(
            pd_number="activity.result.result_link.intervention.number",
            pd_title="activity.result.result_link.intervention.title",
            partner="activity.result.result_link.intervention.agreement.partner.organization.name",
            partner_cso_type="activity.result.result_link.intervention.agreement.partner.organization.cso_type",
            partner_type="activity.result.result_link.intervention.agreement.partner.organization.organization_type",
            partner_vendor_number="activity.result.result_link.intervention.agreement.partner.organization.vendor_number",
            activity="activity.name",
            activity_details="activity.context_details",
            activity_unicef_cash="activity.unicef_cash",
            activity_cso_cash="activity.cso_cash",
            activity_unfunded_cash="activity.unfunded_cash",
            activity_code="activity.code",
            ll_name="activity.result.name",
            ll_code="activity.result.code",
        )
        queryset = lambda: ReportsInterventionactivityitem.objects.select_related(
            "activity__result__result_link__intervention__agreement__partner__organization"
        )

    # ReportsInterventionactivity ** LL, CP, INT, PART
    # ReportsInterventionactivityTimeFrames **
    # ReportsInterventionactivityitem
    # ReportsInterventiontimeframe
