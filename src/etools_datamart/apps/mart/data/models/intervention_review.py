# PartnersInterventionreview
# PartnersPrcofficerinterventionreview
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Intervention
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention_epd import InterventionSimpleAbstract
from etools_datamart.apps.sources.etools.models import PartnersInterventionreview


class InterventionReviewLoader(EtoolsLoader):
    pass


class InterventionReview(InterventionSimpleAbstract, EtoolsDataMartModel):
    loader = InterventionReviewLoader()

    class Options:
        source = PartnersInterventionreview
        depends = (Intervention,)
        mapping = dict()
        queryset = lambda: PartnersInterventionreview.objects.all()
