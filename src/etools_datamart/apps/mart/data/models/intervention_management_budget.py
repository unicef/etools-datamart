# PartnersInterventionmanagementbudget
# PartnersInterventionmanagementbudgetitem
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Intervention
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention_epd import InterventionSimpleAbstract
from etools_datamart.apps.sources.etools.models import PartnersInterventionmanagementbudgetitem


class InterventionManagementBudgetLoader(EtoolsLoader):
    pass


class InterventionManagementBudget(InterventionSimpleAbstract, EtoolsDataMartModel):
    loader = InterventionManagementBudgetLoader()

    class Options:
        source = PartnersInterventionmanagementbudgetitem
        depends = (Intervention,)
        mapping = dict()
        queryset = lambda: PartnersInterventionmanagementbudgetitem.objects.all()
