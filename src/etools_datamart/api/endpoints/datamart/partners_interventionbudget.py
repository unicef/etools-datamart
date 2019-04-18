from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models import Intervention
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import models, PartnersInterventionbudget


class InterventionBudgetLoader(Loader):
    pass


class InterventionBudget(DataMartModel):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    partner_contribution = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    in_kind_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    partner_contribution_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_cash_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    in_kind_amount_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=4, blank=True, null=True)

    intervention_title = models.CharField(max_length=256, blank=True, null=True)
    intervention_number = models.CharField(max_length=64, blank=True, null=True)
    intervention = models.ForeignKey(Intervention,
                                     blank=True, null=True,
                                     on_delete=models.SET_NULL)
    intervention_source_id = models.IntegerField(blank=True, null=True)

    class Options:
        source = PartnersInterventionbudget
        mapping = dict(intervention_title='intervention.title',
                       intervention_number='intervention.number',
                       intervention_source_id='intervention.id',
                       intervention=lambda laoder, record: Intervention.objects.filter(source_id=record.intervention.id).first(),
                       )
