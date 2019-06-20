from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.data.models.intervention import InterventionAbstract, InterventionLoader
from etools_datamart.apps.data.models.mixins import extend
from etools_datamart.apps.etools.models import models, PartnersInterventionbudget


class InterventionBudgetLoader(InterventionLoader):
    pass


class InterventionBudget(InterventionAbstract, DataMartModel):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    budget_cso_contribution = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_currency = models.CharField(max_length=4, blank=True, null=True)
    budget_total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_supply = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    fr_number = models.CharField(max_length=100, blank=True, null=True)

    loader = InterventionBudgetLoader()

    class Options(InterventionAbstract.Options):
        model = PartnersInterventionbudget
        mapping = extend(InterventionAbstract.Options.mapping,
                         dict(
                             budget_cso_contribution='partner_contribution',
                             budget_unicef_cash='unicef_cash',
                             budget_total='total',
                             budget_currency='currency',
                             budget_unicef_supply='in_kind_amount',
                         ))
