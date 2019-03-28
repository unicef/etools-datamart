
from etools_datamart.apps.etools.enrichment.consts import T2FTravelConsts
from etools_datamart.apps.etools.models import T2FTravel

T2FTravel.PLANNED = T2FTravelConsts.PLANNED
T2FTravel.SUBMITTED = T2FTravelConsts.SUBMITTED
T2FTravel.REJECTED = T2FTravelConsts.REJECTED
T2FTravel.APPROVED = T2FTravelConsts.APPROVED
T2FTravel.CANCELLED = T2FTravelConsts.CANCELLED
T2FTravel.SENT_FOR_PAYMENT = T2FTravelConsts.SENT_FOR_PAYMENT
T2FTravel.CERTIFICATION_SUBMITTED = T2FTravelConsts.CERTIFICATION_SUBMITTED
T2FTravel.CERTIFICATION_APPROVED = T2FTravelConsts.CERTIFICATION_APPROVED
T2FTravel.CERTIFICATION_REJECTED = T2FTravelConsts.CERTIFICATION_REJECTED
T2FTravel.CERTIFIED = T2FTravelConsts.CERTIFIED
T2FTravel.COMPLETED = T2FTravelConsts.COMPLETED

T2FTravel._meta.get_field('status').choices = T2FTravelConsts.CHOICES
