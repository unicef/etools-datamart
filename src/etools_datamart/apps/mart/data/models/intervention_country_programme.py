# PartnersInterventionreview
# PartnersInterventionreviewPrcOfficers
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Intervention
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention_epd import InterventionSimpleAbstract
from etools_datamart.apps.sources.etools.models import PartnersInterventionCountryProgrammes


class InterventionCountryProgrammeLoader(EtoolsLoader):
    pass


class InterventionCountryProgramme(InterventionSimpleAbstract, EtoolsDataMartModel):
    loader = InterventionCountryProgrammeLoader()

    class Options:
        source = PartnersInterventionCountryProgrammes
        depends = (Intervention,)
        mapping = dict()
        queryset = lambda: PartnersInterventionCountryProgrammes.objects.all()
