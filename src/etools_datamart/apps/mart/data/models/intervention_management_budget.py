# PartnersInterventionmanagementbudget
# PartnersInterventionmanagementbudgetitem
from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Intervention
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention_epd import InterventionSimpleAbstract
from etools_datamart.apps.sources.etools.models import (
    PartnersInterventionmanagementbudget,
    PartnersInterventionmanagementbudgetitem,
)


class InterventionManagementBudgetLoader(EtoolsLoader):
    pass


class InterventionManagementBudget(InterventionSimpleAbstract, EtoolsDataMartModel):
    # management budget fields
    budget_created = models.DateTimeField()
    budget_modified = models.DateTimeField()
    act1_unicef = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    act1_partner = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # act1_unfunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    act2_unicef = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    act2_partner = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # act2_unfunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    act3_unicef = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    act3_partner = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # act3_unfunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # management budget item fields
    name = models.CharField(max_length=255, blank=True, null=True)
    kind = models.CharField(max_length=15, blank=True, null=True)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    cso_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # unfunded_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    no_units = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=150, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    loader = InterventionManagementBudgetLoader()

    class Options:
        source = PartnersInterventionmanagementbudgetitem
        depends = (Intervention,)
        mapping = dict(
            pd_number="budget.intervention.number",
            pd_title="budget.intervention.title",
            partner="budget.intervention.agreement.partner.organization.name",
            partner_cso_type="budget.intervention.agreement.partner.organization.cso_type",
            partner_type="budget.intervention.agreement.partner.organization.organization_type",
            partner_vendor_number="budget.intervention.agreement.partner.organization.vendor_number",
            # budget fields
            budget_created="budget.created",
            budget_modified="budget.modified",
            act1_unicef="budget.act1_unicef",
            act1_partner="budget.act1_partner",
            # act1_unfunded="budget.act1_unfunded",
            act2_unicef="budget.act2_unicef",
            act2_partner="budget.act2_partner",
            # act2_unfunded="budget.act2_unfunded",
            act3_unicef="budget.act3_unicef",
            act3_partner="budget.act3_partner",
            # act3_unfunded="budget.act3_unfunded",
        )
        queryset = lambda: PartnersInterventionmanagementbudgetitem.objects.select_related(
            "budget", "budget__intervention"
        )
