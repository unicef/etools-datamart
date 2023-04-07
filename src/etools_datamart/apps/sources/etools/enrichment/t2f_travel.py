from etools_datamart.apps.sources.etools.enrichment.consts import T2FTravelConsts
from etools_datamart.apps.sources.etools.models import T2FTravel

from .utils import create_alias

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

T2FTravel._meta.get_field("status").choices = T2FTravelConsts.CHOICES

aliases = (["t2ftravel_t2f_travelattachment_travel_id", "attachments"],)
create_alias(T2FTravel, aliases)


def get_reference_number(self, country):
    return self.reference_number


T2FTravel.get_reference_number = get_reference_number


@property
def task_number(self):
    return list(self.travel.activities.values_list("id", flat=True)).index(self.id) + 1
