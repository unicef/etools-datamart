"""
Country  CoreCountry.name
Partner  PartnerPartner.title
PD       Programmedocument
Indicator Target Reportable.target
Indicator Baseline  Reportable.baseline
Title of Indicator
Calculation across periods  IndicatorReport
Calculation across locations
Means of Verification  Reportable.means_of_verification
Indicator Results level
Indicator Location Name  IndicatorLocationData.location.name
Indicator Location Geo   IndicatorLocationData.location.point
Admin level of location  IndicatorLocationData.location.type.admin_level
Frequency  IndicatorReport.frequency / Reportable / ProgrammeDocument
Overall Status  ProgressReport.review_overall_status
Narrative Assessment  IndicatorReport.narrative_assessment
Due date  IndicatorReport.due_date
Submission date  IndicatorReport.submission_date
Project activity  ??PartnerActivity??
Totalbudget(ideally at most granular level tied to activity / result)
Utilised budget(same conditions as above)
Report  #
"""
from .base import PrpDataMartModel


class ValueForMoney(PrpDataMartModel):
    pass
