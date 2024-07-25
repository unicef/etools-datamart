from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import JSONField, Prefetch

from celery.utils.log import get_task_logger

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.models import Location
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention import InterventionAbstract, InterventionLoader
from etools_datamart.apps.sources.etools.enrichment.consts import PartnersInterventionConst, TravelType
from etools_datamart.apps.sources.etools.models import (
    AuthUser,
    DjangoContentType,
    FundsFundsreservationheader,
    LocationsLocation,
    models,
    PartnersFiletype,
    PartnersIntervention,
    PartnersInterventionamendment,
    PartnersInterventionattachment,
    PartnersInterventionbudget,
    PartnersInterventionFlatLocations,
    PartnersInterventionOffices,
    PartnersInterventionPartnerFocalPoints,
    PartnersInterventionplannedvisits,
    PartnersInterventionresultlink,
    PartnersInterventionSections,
    PartnersInterventionUnicefFocalPoints,
    PartnersPartnerorganization,
    ReportsAppliedindicator,
    ReportsLowerresult,
    ReportsOffice,
    ReportsResult,
    ReportsSector,
    T2FTravelactivity,
    UsersUserprofile,
)

logger = get_task_logger(__name__)


class InterventionBudgetLoader(InterventionLoader):
    def get_queryset(self):
        return (
            PartnersInterventionbudget.objects.exclude(intervention__isnull=True)
            .select_related(
                "intervention",
                "intervention__unicef_signatory",
                "intervention__agreement",
                "intervention__agreement__partner",
                "intervention__agreement__partner__organization",
                "intervention__country_programme",
                "intervention__partner_authorized_officer_signatory",
            )
            .prefetch_related(
                Prefetch(
                    "intervention__FundsFundsreservationheader_intervention",
                    queryset=FundsFundsreservationheader.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionamendment_intervention",
                    queryset=PartnersInterventionamendment.objects.all().order_by("signed_date"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionattachment_intervention",
                    queryset=PartnersInterventionattachment.objects.all().only(
                        "id",
                        "intervention_id",
                        "type_id",
                    ),
                ),
                Prefetch(
                    "intervention__PartnersInterventionattachment_intervention__type",
                    queryset=PartnersFiletype.objects.all().only(
                        "id",
                        "name",
                    ),
                ),
                Prefetch(
                    "intervention__PartnersInterventionplannedvisits_intervention",
                    queryset=PartnersInterventionplannedvisits.objects.filter(year=self.context["today"].year),
                ),
                Prefetch(
                    "intervention__PartnersInterventionresultlink_intervention__ReportsLowerresult_result_link__ReportsAppliedindicator_lower_result",
                    queryset=ReportsAppliedindicator.objects.all(),
                ),
                Prefetch(
                    "intervention__T2FTravelactivity_partnership",
                    queryset=T2FTravelactivity.objects.filter(
                        travel_type=TravelType.PROGRAMME_MONITORING,
                        travels__status="completed",
                        date__isnull=False,
                    ).order_by("date"),
                ),
                Prefetch(
                    "intervention__country_programme__ReportsResult_country_programme",
                    queryset=ReportsResult.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionSections_intervention",
                    queryset=PartnersInterventionSections.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionSections_intervention__section",
                    queryset=ReportsSector.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionOffices_intervention__office",
                    queryset=ReportsOffice.objects.all().order_by("id"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionUnicefFocalPoints_intervention",
                    queryset=PartnersInterventionUnicefFocalPoints.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionUnicefFocalPoints_intervention__user",
                    queryset=AuthUser.objects.only("id", "username", "first_name", "last_name", "email"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionPartnerFocalPoints_intervention",
                    queryset=PartnersInterventionPartnerFocalPoints.objects.only("id", "intervention_id", "user_id"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionPartnerFocalPoints_intervention__user",
                    queryset=AuthUser.objects.only("id", "username", "first_name", "last_name", "email", "profile"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionPartnerFocalPoints_intervention__user__profile",
                    queryset=UsersUserprofile.objects.only("id", "phone_number", "user_id"),
                ),
                Prefetch(
                    "intervention__PartnersInterventionFlatLocations_intervention",
                    queryset=PartnersInterventionFlatLocations.objects.all(),
                ),
                Prefetch(
                    "intervention__PartnersInterventionFlatLocations_intervention__location",
                    queryset=LocationsLocation.objects.only(
                        "id",
                        "name",
                        "admin_level",
                        "p_code",
                        "latitude",
                        "admin_level_name",
                        "longitude",
                    ),
                ),
                Prefetch(
                    "intervention__PartnersInterventionresultlink_intervention__cp_output",
                    queryset=ReportsResult.objects.only("id", "name", "wbs"),
                ),
            )
        )

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")
        qs = self.get_queryset()

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for record in page.object_list:
                filters = self.config.key(self, record)
                values = self.get_values(record.intervention)
                values["source_id"] = record.id
                values["budget_cso_contribution"] = record.partner_contribution_local
                values["budget_unicef_cash"] = record.unicef_cash_local
                # values["budget_total_unfunded"] = record.total_unfunded
                values["budget_total"] = record.total_local
                values["budget_currency"] = record.currency
                values["budget_unicef_supply"] = record.in_kind_amount_local
                op = self.process_record(filters, values)
                self.increment_counter(op)


class InterventionBudget(InterventionAbstract, EtoolsDataMartModel):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    budget_cso_contribution = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_currency = models.CharField(max_length=5, blank=True, null=True)
    budget_total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # budget_total_unfunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    budget_unicef_supply = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    fr_numbers = models.TextField(max_length=100, blank=True, null=True)
    fr_numbers_data = JSONField(blank=True, null=True, default=dict)

    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True, default=dict)

    loader = InterventionBudgetLoader()

    class Meta:
        ordering = ("-created",)

    class Options(InterventionAbstract.Options):
        model = PartnersInterventionbudget
        depends = (Location,)
        key = lambda loader, record: dict(schema_name=loader.context["country"].schema_name, source_id=record.pk)
