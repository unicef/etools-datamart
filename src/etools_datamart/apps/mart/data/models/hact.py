import json

from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import HactAggregatehact


class HACTLoader(EtoolsLoader):
    """
    --
    SET search_path = public, ##COUNTRY##;

    --
    --
    --FOR EACH ##YEAR##  IN (2018, 2019. 2020, 2021,...  <THIS YEAR>)
    --Perform following;
    SELECT '##COUNTRY##' AS __schema,
           "hact_aggregatehact"."id",
           "hact_aggregatehact"."created",
           "hact_aggregatehact"."modified",
           "hact_aggregatehact"."year",
           "hact_aggregatehact"."partner_values"
    FROM "hact_aggregatehact"
    WHERE "hact_aggregatehact"."year" =##YEAR##)
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

    --NOTE:
    --When available JSON properties are to be retrieved;
    --"hact_aggregatehact"."partner_values"["assurance_activities"]["micro_assessment"],
    --"hact_aggregatehact"."partner_values"["assurance_activities"]["programmatic_visits"]["completed"],
    --"hact_aggregatehact"."partner_values"["assurance_activities"]["spot_checks"]["follow_up"],
    --"hact_aggregatehact"."partner_values"["assurance_activities"]["spot_checks"]["completed"],
    --"hact_aggregatehact"."partner_values"["assurance_activities"]["scheduled_audit"],
    --"hact_aggregatehact"."partner_values"["assurance_activities"]["special_audit"]
    """

    def get_queryset(self):
        return self.config.source.objects.filter(year=self.context["year"])
        # return HactAggregatehact.objects.filter(year=self.context['year'])

    def process_country(self):
        # TODO: Analyze more before batch processing
        country = self.context["country"]
        for year in range(2018, self.context["today"].year + 1):
            self.context["year"] = year
            try:
                aggregate = self.get_queryset().get()
                data = (
                    json.loads(aggregate.partner_values)
                    if isinstance(aggregate.partner_values, str)
                    else aggregate.partner_values
                )

                # # Total number of completed Microassessments in the business area in the past year
                values = dict(
                    microassessments_total=data["assurance_activities"]["micro_assessment"],
                    programmaticvisits_total=data["assurance_activities"]["programmatic_visits"]["completed"],
                    followup_spotcheck=data["assurance_activities"]["spot_checks"]["follow_up"],
                    completed_spotcheck=data["assurance_activities"]["spot_checks"]["completed"],
                    completed_hact_audits=data["assurance_activities"]["scheduled_audit"],
                    completed_special_audits=data["assurance_activities"]["special_audit"],
                    seen=self.context["today"],
                    area_code=country.business_area_code,
                    schema_name=country.schema_name,
                )
                op = self.process_record(
                    filters=dict(
                        year=year,
                        # area_code=country.business_area_code,
                        country_name=country.name,
                        # schema_name=country.schema_name
                    ),
                    values=values,
                )
                self.increment_counter(op)
            except HactAggregatehact.DoesNotExist:  # pragma: no cover
                pass


class HACT(EtoolsDataMartModel):
    year = models.IntegerField()
    microassessments_total = models.IntegerField(
        default=0, help_text="Total number of completed Microassessments in the business area in the past year"
    )
    programmaticvisits_total = models.IntegerField(
        default=0, help_text="Total number of completed Programmatic visits in the business area"
    )
    followup_spotcheck = models.IntegerField(
        default=0, help_text="Total number of completed Programmatic visits in the business area"
    )
    completed_spotcheck = models.IntegerField(
        default=0, help_text="Total number of completed Programmatic visits in the business area"
    )
    completed_hact_audits = models.IntegerField(
        default=0, help_text="Total number of completed scheduled audits for the workspace."
    )
    completed_special_audits = models.IntegerField(
        default=0, help_text="Total number of completed special audits for the workspace. "
    )

    loader = HACTLoader()

    class Meta:
        ordering = ("year", "country_name")
        unique_together = ("year", "country_name")
        verbose_name = "HACT"

    class Options:
        source = HactAggregatehact
        sync_deleted_records = lambda loader: False
        truncate = False
