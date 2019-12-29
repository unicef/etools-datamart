"""
IndicatorLocationData -----
1)
Country                         CoreCountry.name
Partner                         PartnerPartner.title
PD                              UnicefProgrammedocument.reference_number
Indicator Target                Reportable.target
Indicator Baseline              Reportable.baseline
Title of Indicator              Reportable.blueprint.title

d. denominatro
v. enumaror
c. calc

2)
Indicator ID                Reportable.id
Indicator Location Name         IndicatorLocationData.location.name
Indicator Location Geo          IndicatorLocationData.location.point
Admin level of location         IndicatorLocationData.location.type.admin_level
Reported Total                  IndicatorLocationData.disaggregation['()']['c']



Country                         CoreCountry.name
Partner                         PartnerPartner.title
PD                              UnicefProgrammedocument.reference_number
Indicator Target                Reportable.target
Indicator Baseline              Reportable.baseline
Title of Indicator              Reportable.blueprint.title
Calculation across periods      'sum' 'max'...
Calculation across locations    'sum' 'max'....
Means of Verification           Reportable.means_of_verification
Indicator Results level         ???
Indicator Location Name         IndicatorLocationData.location.name
Indicator Location Geo          IndicatorLocationData.location.point
Admin level of location         IndicatorLocationData.location.type.admin_level
Frequency                       IndicatorReport.frequency (Reportable, ProgrammeDocument ??)
Overall Status                  ProgressReport.review_overall_status
Narrative Assessment            IndicatorReport.narrative_assessment
Due date                        IndicatorReport.due_date
Submission date                 IndicatorReport.submission_date
Project activity                (cannot find this field maybe PartnerActivity?)

Totalbudget(ideally at most granular level tied to activity / result)
Utilised budget(same conditions as above)
Report  #
"""
from django.db import models

from .base import PrpDataMartModel


class ValueForMoney(PrpDataMartModel):
    country = models.CharField(max_length=100, blank=True, null=True)
