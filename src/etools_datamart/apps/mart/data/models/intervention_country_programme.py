from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Intervention
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention_epd import InterventionSimpleAbstract
from etools_datamart.apps.sources.etools.models import PartnersInterventionCountryProgrammes


class InterventionCountryProgrammeLoader(EtoolsLoader):
    def get_queryset(self):
        return PartnersInterventionCountryProgrammes.objects.select_related(
            "countryprogramme", "intervention", "intervention__agreement", "intervention__agreement__partner"
        )


class InterventionCountryProgramme(InterventionSimpleAbstract, EtoolsDataMartModel):
    country_programme = models.CharField(max_length=300, blank=True, null=True)

    loader = InterventionCountryProgrammeLoader()

    class Options:
        source = PartnersInterventionCountryProgrammes
        depends = (Intervention,)
        mapping = dict(
            pd_number="intervention.number",
            pd_title="intervention.title",
            partner="intervention.agreement.partner.name",
            partner_cso_type="intervention.agreement.partner.cso_type",
            partner_type="intervention.agreement.partner.partner_type",
            partner_vendor_number="intervention.agreement.partner.vendor_number",
            country_programme="countryprogramme.name",
        )
