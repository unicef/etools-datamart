from django.contrib.postgres.fields import JSONField

from etools_datamart.apps.data.models import Location
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.data.models.intervention import InterventionAbstract, InterventionLoader
from etools_datamart.apps.data.models.mixins import extend
from etools_datamart.apps.etools.models import (FundsFundsreservationheader, models,
                                                PartnersIntervention, PartnersInterventionbudget,)


class InterventionBudgetLoader(InterventionLoader):
    def get_fr_numbers(self, original: PartnersIntervention, values: dict):
        data = []
        ret = []
        for fr in FundsFundsreservationheader.objects.filter(intervention=original):
            ret.append(fr.fr_number)
            data.append(dict(fr_number=fr.fr_number,
                             vendor_code=fr.vendor_code,
                             fr_type=fr.fr_type,
                             currency=fr.currency,
                             ))

        values['fr_numbers_data'] = data
        return ", ".join(ret)


class InterventionBudget(InterventionAbstract, DataMartModel):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    budget_cso_contribution = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_currency = models.CharField(max_length=4, blank=True, null=True)
    budget_total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_supply = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    fr_numbers = models.TextField(max_length=100, blank=True, null=True)
    fr_numbers_data = JSONField(blank=True, null=True, default=dict)

    loader = InterventionBudgetLoader()

    class Options(InterventionAbstract.Options):
        model = PartnersInterventionbudget
        depends = (Location,)
        mapping = extend(InterventionAbstract.Options.mapping,
                         dict(
                             budget_cso_contribution='partner_contribution',
                             budget_unicef_cash='unicef_cash',
                             budget_total='total',
                             budget_currency='currency',
                             budget_unicef_supply='in_kind_amount',
                         ))
