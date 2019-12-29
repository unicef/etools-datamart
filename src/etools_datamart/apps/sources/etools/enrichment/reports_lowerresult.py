# from django.db import models
#
# from etools_datamart.apps.etools.enrichment.utils import create_alias, set_related_name
# from etools_datamart.apps.etools.models import (LocationsLocation, ReportsAppliedindicator,
#                                                 ReportsAppliedindicatorDisaggregation, ReportsAppliedindicatorLocations,
#                                                 ReportsDisaggregation, ReportsLowerresult)
#
#
# aliases = (['partnersintervention_partners_interventionbudget_intervention_id',
#             'planned_budget'],
#            ['partnersintervention_funds_fundsreservationheader_intervention_id',
#             'frs'],
#            ['partnersintervention_partners_interventionattachment_intervention_id',
#             'attachments'],
#
#            # ['partnersintervention_partners_interventionplannedvisits_intervention_id',
#            #  'planned_visits'],
#
#            )
# create_alias(ReportsLowerresult, aliases)
# partnersinterventionresultlink_reports_lowerresult_result_link_id


# set_related_name(ReportsLowerresult, 'result_link', 'applied_indicators')
