from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import ReportsResult


class Result(EtoolsDataMartModel):
    """
    --
    SET search_path = public, ##PRODUCT##;

    --
    SELECT COUNT(*) AS "__count" FROM "reports_result";

    --
    SELECT 'afghanistan' AS __schema,
          "reports_result"."id",
          "reports_result"."name",                      -- mapped to .name
          "reports_result"."code",                      -- mapped to .code
          "reports_result"."result_type_id",
          "reports_result"."sector_id",
          "reports_result"."gic_code",                  -- mapped to .gic_code
          "reports_result"."gic_name",                  -- mapped to .gic_name
          "reports_result"."humanitarian_tag",          -- mapped to .humanitarian_tag
          "reports_result"."level",
          "reports_result"."lft",
          "reports_result"."parent_id",
          "reports_result"."rght",
          "reports_result"."sic_code",                  -- mapped to .sic_code
          "reports_result"."sic_name",                  -- mapped to .sic_name
          "reports_result"."tree_id",
          "reports_result"."vision_id",
          "reports_result"."wbs",
          "reports_result"."activity_focus_code",       -- mapped to .activity_focus_code
          "reports_result"."activity_focus_name",       -- mapped to .activity_focus_name
          "reports_result"."hidden",
          "reports_result"."from_date",                 -- mapped to .from_date
          "reports_result"."to_date",                   -- mapped to .to_date
          "reports_result"."ram",                       -- mapped to .ram
          "reports_result"."country_programme_id",
          "reports_result"."created",
          "reports_result"."modified",
          "reports_result"."humanitarian_marker_code",  -- mapped to .humanitarian_marker_code
          "reports_result"."humanitarian_marker_name",  -- mapped to .humanitarian_marker_name
          "reports_result"."programme_area_code",       -- mapped to .programme_area_code
          "reports_result"."programme_area_name"        -- mapped to .programme_area_name
    FROM "reports_result"
    ORDER BY "reports_result"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

    --
    SELECT '##COUNTRY##' AS __schema,
          "reports_resulttype"."id",
          "reports_resulttype"."name"                   --  mapped to .result_type
    FROM "reports_resulttype"
    WHERE "reports_resulttype"."id" in (## List of "reports_result"."result_type_id" in the page##);

    --
    SELECT '##COUNTRY##' AS __schema,
          "reports_countryprogramme"."id",
          "reports_countryprogramme"."name",           -- mapped to .country_programme
          "reports_countryprogramme"."wbs",            -- mapped to .wbs
          "reports_countryprogramme"."from_date",
          "reports_countryprogramme"."to_date",
          "reports_countryprogramme"."invalid"
    FROM "reports_countryprogramme"
    WHERE "reports_countryprogramme"."id" in (## List of "reports_result"."country_programme_id" in the page##);


    SELECT id,
           name                                        -- mapped to .section
    FROM ReportsSector
    WHERE id in (## List of "reports_result"."sector_id" in the page ##)

    """

    name = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    result_type = models.CharField(max_length=150, blank=True, null=True)
    section = models.CharField(max_length=128, blank=True, null=True)
    gic_code = models.CharField(max_length=8, blank=True, null=True)
    gic_name = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_tag = models.BooleanField(blank=True, null=True)
    sic_code = models.CharField(max_length=8, blank=True, null=True)
    sic_name = models.CharField(max_length=255, blank=True, null=True)
    wbs = models.CharField(max_length=50, blank=True, null=True)
    activity_focus_code = models.CharField(max_length=8, blank=True, null=True)
    activity_focus_name = models.CharField(max_length=255, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    ram = models.BooleanField(blank=True, null=True)
    country_programme = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_marker_code = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_marker_name = models.CharField(max_length=255, blank=True, null=True)
    programme_area_code = models.CharField(max_length=16, null=True, blank=True)
    programme_area_name = models.CharField(max_length=255, null=True, blank=True)

    loader = EtoolsLoader()

    class Options:
        source = ReportsResult
        mapping = dict(
            result_type="result_type.name",
            section="sector.name",
            country_programme="country_programme.name",
        )
