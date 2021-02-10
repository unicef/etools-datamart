from django.db.models import JSONField

from etools_datamart.apps.mart.data.models import Location
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention import InterventionAbstract, InterventionLoader
from etools_datamart.apps.sources.etools.models import (
    FundsFundsreservationheader,
    models,
    PartnersIntervention,
    PartnersInterventionbudget,
)


class InterventionBudgetLoader(InterventionLoader):
    def get_queryset(self):
        return PartnersInterventionbudget.objects

    def process_country(self):
        for record in self.get_queryset().all():
            filters = self.config.key(self, record)
            values = self.get_values(record.intervention)
            values['source_id'] = record.id
            values['budget_cso_contribution'] = record.partner_contribution_local
            values['budget_unicef_cash'] = record.unicef_cash_local
            values['budget_total'] = record.total_local
            values['budget_currency'] = record.currency
            values['budget_unicef_supply'] = record.in_kind_amount_local
            op = self.process_record(filters, values)
            self.increment_counter(op)

    def get_fr_numbers(self, record: PartnersIntervention, values: dict, **kwargs):
        data = []
        ret = []
        for fr in FundsFundsreservationheader.objects.filter(intervention=record):
            ret.append(fr.fr_number)
            data.append(dict(fr_number=fr.fr_number,
                             vendor_code=fr.vendor_code,
                             fr_type=fr.fr_type,
                             currency=fr.currency,
                             ))

        values['fr_numbers_data'] = data
        return ", ".join(ret)


class InterventionBudget(InterventionAbstract, EtoolsDataMartModel):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    budget_cso_contribution = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_currency = models.CharField(max_length=5, blank=True, null=True)
    budget_total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_supply = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    fr_numbers = models.TextField(max_length=100, blank=True, null=True)
    fr_numbers_data = JSONField(blank=True, null=True, default=dict)

    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True, default=dict)

    loader = InterventionBudgetLoader()

    class Meta:
        ordering = ("-created",)

    class Options(InterventionAbstract.Options):
        model = PartnersInterventionbudget
        depends = (Location,)
        key = lambda loader, record: dict(schema_name=loader.context['country'].schema_name,
                                          source_id=record.pk)
