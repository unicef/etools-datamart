from django.db import models

from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import ReportsSector


class Section(EtoolsDataMartModel):
    """
    --
    SET search_path = public, ##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count" FROM "reports_sector";

    --
    SELECT '##COUNTRY##' AS __schema,
           "reports_sector"."id",                -- mapped to  .source_id
           "reports_sector"."name",              -- mapped to .name
           "reports_sector"."description",       -- mapped to .description
           "reports_sector"."alternate_id",      -- mapped to .alternate_id
           "reports_sector"."alternate_name",    -- mapped to .alternate_name
           "reports_sector"."dashboard",         -- mapped to .dashboard
           "reports_sector"."color",             -- mapped to .color
           "reports_sector"."created",           -- mapped to .created
           "reports_sector"."modified",          -- mapped to .modified
           "reports_sector"."active"
    FROM "reports_sector" ORDER BY "reports_sector"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;
    """

    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    alternate_id = models.IntegerField(blank=True, null=True)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    dashboard = models.BooleanField(null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Options:
        source = ReportsSector
