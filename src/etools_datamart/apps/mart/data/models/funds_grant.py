from django.db import models

from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import FundsGrant

"""
--
SET search_path = public,##COUNTRY##;

--
SELECT COUNT(*) AS "__count"
FROM "funds_grant";

--
SELECT '##COUNTRY##' AS __schema,
       "funds_grant"."id",   
       "funds_grant"."name",
       "funds_grant"."donor_id",
       "funds_grant"."expiry",
       "funds_grant"."description",
       "funds_grant"."created",
       "funds_grant"."modified"
FROM "funds_grant"
ORDER BY "funds_grant"."id" ASC 
LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

--
SELECT '##COUNTRY##' AS __schema,
       "funds_donor"."id",
       "funds_donor"."name",
       "funds_donor"."created",
       "funds_donor"."modified"
       FROM "funds_donor"
WHERE "funds_donor"."id" IN (## LIST OF "funds_grant"."donor_id" IN THE PAGE ##);
"""


class Grant(EtoolsDataMartModel):
    name = models.CharField(max_length=128, blank=True, null=True)
    donor = models.CharField(max_length=128, blank=True, null=True)
    expiry = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Options:
        source = FundsGrant
        mapping = dict(donor="donor.name")
