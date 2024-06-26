import datetime
import logging

from django.conf import settings
from django.core.paginator import Paginator
from django.db import models
from django.db.models import F, JSONField, Sum
from django.utils.functional import cached_property

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.reports_office import Office
from etools_datamart.apps.sources.etools.enrichment.consts import PartnersInterventionConst, TravelType
from etools_datamart.apps.sources.etools.models import (
    DjangoContentType,
    FundsFundsreservationheader,
    PartnersIntervention,
    PartnersInterventionamendment,
    PartnersInterventionplannedvisits,
    ReportsAppliedindicator,
    T2FTravelactivity,
)

from .base import EtoolsDataMartModel
from .location import Location
from .mixins import add_location_mapping, LocationMixin, NestedLocationLoaderMixin, NestedLocationMixin
from .partner import Partner

logger = logging.getLogger(__name__)


class InterventionAbstract(models.Model):
    agreement_reference_number = models.CharField(max_length=300, blank=True, null=True)
    amendment_types = models.TextField(blank=True, null=True)
    attachment_types = models.TextField(blank=True, null=True)
    agreement_id = models.IntegerField(blank=True, null=True)
    cfei_number = models.CharField(max_length=150, null=True, blank=True)
    clusters = models.TextField(blank=True, null=True)
    contingency_pd = models.BooleanField(null=True)
    cp_outputs = models.TextField(blank=True, null=True)
    cp_outputs_data = JSONField(blank=True, null=True, default=dict)

    cso_type = models.CharField(max_length=300, blank=True, null=True)
    country_programme = models.CharField(max_length=300, blank=True, null=True)
    country_programme_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    currency = models.CharField(max_length=5, blank=True, null=True)
    days_from_prc_review_to_signature = models.IntegerField(blank=True, null=True)
    days_from_submission_to_signature = models.IntegerField(blank=True, null=True)
    document_type = models.CharField(max_length=255, null=True, choices=PartnersInterventionConst.INTERVENTION_TYPES)
    end_date = models.DateField(null=True)
    fr_number = models.CharField(max_length=300, blank=True, null=True)
    outstanding_amt_local = models.DecimalField(default=0, max_digits=20, decimal_places=2, blank=True, null=True)
    in_kind_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    in_kind_amount_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    intervention_id = models.IntegerField(blank=True, null=True)
    last_amendment_date = models.DateField(blank=True, null=True)
    metadata = JSONField(blank=True, null=True, default=dict)
    number = models.CharField(max_length=64, null=True)
    number_of_attachments = models.IntegerField(blank=True, null=True)
    number_of_amendments = models.IntegerField(blank=True, null=True)
    offices = models.TextField(blank=True, null=True)
    offices_data = JSONField(blank=True, null=True, default=dict)
    partner_authorized_officer_signatory_id = models.IntegerField(null=True)
    partner_contribution = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    partner_contribution_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    partner_focal_points = models.TextField(blank=True, null=True)
    partner_focal_points_data = JSONField(blank=True, null=True, default=dict)
    # partner_focal_point_email = models.CharField(max_length=128, null=True)
    # partner_focal_point_first_name = models.CharField(max_length=64, null=True)
    # partner_focal_point_last_name = models.CharField(max_length=64, null=True)
    # partner_focal_point_phone = models.CharField(max_length=64, null=True)
    # partner_focal_point_title = models.CharField(max_length=64, null=True)
    partner_id = models.IntegerField(blank=True, null=True)
    partner_name = models.CharField(max_length=200, null=True)
    partner_sea_risk_rating = models.CharField(max_length=150, null=True, blank=True)
    partner_signatory_name = models.CharField(max_length=300, null=True)
    partner_signatory_email = models.CharField(max_length=128, null=True)
    partner_signatory_first_name = models.CharField(max_length=64, null=True)
    partner_signatory_last_name = models.CharField(max_length=64, null=True)
    partner_signatory_phone = models.CharField(max_length=64, null=True)
    partner_signatory_title = models.CharField(max_length=100, null=True)
    partner_source_id = models.IntegerField(blank=True, null=True)
    partner_type = models.CharField(max_length=64, null=True)
    partner_vendor_number = models.CharField(max_length=100, blank=True, null=True)
    planned_programmatic_visits = models.IntegerField(blank=True, null=True)
    population_focus = models.CharField(max_length=130, null=True)
    prc_review_document = models.CharField(max_length=1024, null=True)
    review_date_prc = models.DateField(null=True)
    reference_number = models.CharField(max_length=100, null=True)
    sections = models.TextField(blank=True, null=True)
    sections_data = JSONField(blank=True, null=True, default=dict)
    signed_by_partner_date = models.DateField(null=True)
    signed_by_unicef_date = models.DateField(null=True)
    signed_pd_document = models.CharField(max_length=1024, null=True)
    start_date = models.DateField(null=True)
    status = models.CharField(max_length=32, null=True, db_index=True, choices=PartnersInterventionConst.STATUSES)
    submission_date = models.DateField(null=True)
    submission_date_prc = models.DateField(null=True)
    title = models.CharField(max_length=306, null=True, db_index=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # has_unfunded_cash = models.BooleanField(null=True)
    # total_unfunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_cash_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    unicef_focal_points = models.TextField(blank=True, null=True)
    unicef_focal_points_data = JSONField(blank=True, null=True, default=dict)
    unicef_signatory_name = models.CharField(max_length=500, null=True)
    # unicef_signatory_first_name = models.CharField(max_length=30, null=True)
    # unicef_signatory_id = models.IntegerField(blank=True, null=True)
    # unicef_signatory_last_name = models.CharField(max_length=30, null=True)
    updated = models.DateTimeField(null=True)
    last_pv_date = models.DateField(null=True, blank=True)

    has_activities_involving_children = models.BooleanField(null=True)
    has_data_processing_agreement = models.BooleanField(null=True)
    has_special_conditions_for_construction = models.BooleanField(null=True)
    final_review_approved = models.BooleanField(null=True)
    other_details = models.TextField(blank=True, null=True)

    # disbursement_percent = models.IntegerField('Disbursement To Date (%)')

    class Meta:
        abstract = True

    class Options:
        depends = (Office, Location, Partner)
        source = PartnersIntervention
        queryset = lambda: PartnersIntervention.objects.select_related(
            "agreement",
            "partner_authorized_officer_signatory",
            "unicef_signatory",
            "country_programme",
            "partnersintervention_partners_interventionbudget_intervention_id",
        )
        key = lambda loader, record: dict(schema_name=loader.context["country"].schema_name, intervention_id=record.pk)
        mapping = dict(
            agreement_reference_number="agreement.reference_number",
            amendment_types="-",
            attachment_types="-",
            clusters="-",
            contingency_pd="=",
            country_programme="country_programme.name",
            country_programme_id="country_programme.pk",
            cp_outputs="-",
            created="=",
            cso_type="agreement.partner.organization.cso_type",
            currency="PartnersInterventionbudget_intervention.currency",
            days_from_submission_to_signature="-",
            days_from_prc_review_to_signature="-",
            end_date="end",
            fr_number="-",
            outstanding_amt_local="-",
            in_kind_amount="PartnersInterventionbudget_intervention.in_kind_amount",
            in_kind_amount_local="PartnersInterventionbudget_intervention.in_kind_amount_local",
            intervention_id="id",
            last_amendment_date="i",
            last_pv_date="-",
            location="i",
            # locations_data='i',
            # locations='-',
            number_of_amendments="i",
            number_of_attachments="i",
            offices="-",
            offices_data="i",
            partner_authorized_officer_signatory_id="partner_authorized_officer_signatory.pk",
            partner_contribution="PartnersInterventionbudget_intervention.partner_contribution",
            partner_contribution_local="PartnersInterventionbudget_intervention.partner_contribution_local",
            partner_focal_points="-",
            partner_focal_points_data="i",
            partner_id="-",
            partner_name="agreement.partner.organization.name",
            partner_sea_risk_rating="i",
            partner_signatory_email="partner_authorized_officer_signatory.email",
            partner_signatory_first_name="partner_authorized_officer_signatory.first_name",
            partner_signatory_last_name="partner_authorized_officer_signatory.last_name",
            partner_signatory_phone="partner_authorized_officer_signatory.phone",
            partner_signatory_title="partner_authorized_officer_signatory.title",
            partner_source_id="agreement.partner.id",
            partner_type="agreement.partner.organization.organization_type",
            partner_vendor_number="agreement.partner.organization.vendor_number",
            planned_programmatic_visits="-",
            prc_review_document="-",
            sections="-",
            start_date="start",
            status="=",
            total="PartnersInterventionbudget_intervention.total",
            # has_unfunded_cash="PartnersInterventionbudget_intervention.has_unfunded_cash",
            # total_unfunded="PartnersInterventionbudget_intervention.total_unfunded",
            total_local="PartnersInterventionbudget_intervention.total_local",
            unicef_cash="PartnersInterventionbudget_intervention.unicef_cash",
            unicef_cash_local="PartnersInterventionbudget_intervention.unicef_cash_local",
            unicef_focal_points="-",
            unicef_focal_points_data="i",
            # unicef_signatory_email='unicef_signatory.email',
            # unicef_signatory_first_name='unicef_signatory.first_name',
            # unicef_signatory_id='unicef_signatory.pk',
            # unicef_signatory_last_name='unicef_signatory.last_name',
            updated="modified",
            cfei_number="=",
        )


class InterventionLoader(NestedLocationLoaderMixin, EtoolsLoader):
    location_m2m_field = "flat_locations"

    def get_queryset(self):
        return PartnersIntervention.objects.select_related("agreement", "agreement__partner").prefetch_related(
            "sections", "flat_locations", "offices", "unicef_focal_points", "partner_focal_points", "result_links"
        )

    @cached_property
    def _ct(self):
        return DjangoContentType.objects.get(app_label="partners", model="intervention").model

    # def fr_currencies_ok(self, original: PartnersIntervention):
    #     return original.frs__currency__count == 1 if original.frs__currency__count else None

    def get_partner_id(self, record: PartnersIntervention, values: dict, **kwargs):
        try:
            data = Partner.objects.get(
                schema_name=self.context["country"].schema_name,
                source_id=record.agreement.partner.id,
            )
            values["partner_sea_risk_rating"] = data.sea_risk_rating_name
            return data.pk
        except Partner.DoesNotExist:
            values["partner_sea_risk_rating"] = None
            return None

    def get_planned_programmatic_visits(self, record: PartnersIntervention, values: dict, **kwargs):
        qs = PartnersInterventionplannedvisits.objects.filter(intervention=record)
        qs = qs.filter(year=self.context["today"].year)
        qs = qs.annotate(
            planned=F("programmatic_q1") + F("programmatic_q2") + F("programmatic_q3") + F("programmatic_q4")
        )
        record = qs.first()
        if record:
            return record.planned

    def get_attachment_types(self, record: PartnersIntervention, values: dict, **kwargs):
        qs = record.PartnersInterventionattachment_intervention.all()
        values["number_of_attachments"] = qs.count()
        return ", ".join(qs.values_list("type__name", flat=True))

    def get_amendment_types(self, record: PartnersIntervention, values: dict, **kwargs):
        qs = PartnersInterventionamendment.objects.filter(intervention=record).order_by("signed_date")
        values["number_of_amendments"] = qs.count()
        if qs:
            values["last_amendment_date"] = qs.latest("signed_date").signed_date
        types = [str(t) for t in qs.values_list("types", flat=True)]
        return ", ".join(types)

    def get_days_from_prc_review_to_signature(self, record: PartnersIntervention, values: dict, **kwargs):
        i1 = record.review_date_prc
        i2 = record.signed_by_partner_date
        if i1 and i2:
            return (i2 - i1).days

    def get_days_from_submission_to_signature(self, record: PartnersIntervention, values: dict, **kwargs):
        i1 = record.submission_date
        i2 = record.signed_by_unicef_date
        if i1 and i2:
            return (i2 - i1).days

    def get_sections(self, record: PartnersIntervention, values: dict, **kwargs):
        data = []
        for section in record.sections.all():
            data.append(
                dict(
                    source_id=section.id,
                    name=section.name,
                    description=section.description,
                )
            )
        values["sections_data"] = data
        return ", ".join([sec["name"] for sec in data])

    def get_last_pv_date(self, record: PartnersIntervention, values: dict, **kwargs):
        ta = (
            T2FTravelactivity.objects.filter(
                partnership__pk=record.pk,
                travel_type=TravelType.PROGRAMME_MONITORING,
                travels__status="completed",
                date__isnull=False,
            )
            .order_by("date")
            .last()
        )
        return ta.date if ta else None

    def get_unicef_signatory_name(self, record: PartnersIntervention, values: dict, **kwargs):
        if record.unicef_signatory:
            return "{0.username} ({0.email})".format(record.unicef_signatory)

    def get_partner_signatory_name(self, record: PartnersIntervention, values: dict, **kwargs):
        if record.partner_authorized_officer_signatory:
            return "{0.last_name} {0.first_name} ({0.email})".format(record.partner_authorized_officer_signatory)

    def get_offices(self, record: PartnersIntervention, values: dict, **kwargs):
        # PartnersInterventionOffices
        data = []
        for office in record.offices.order_by("id"):
            data.append(
                dict(
                    source_id=office.id,
                    name=office.name,
                )
            )
        values["offices_data"] = data
        return ", ".join([off["name"] for off in data])

    def get_clusters(self, record: PartnersIntervention, values: dict, **kwargs):
        qs = ReportsAppliedindicator.objects.filter(lower_result__result_link__intervention=record)
        clusters = set()
        for applied_indicator in qs.all():
            if applied_indicator.cluster_name:
                clusters.add(applied_indicator.cluster_name)
        return ", ".join(clusters)

    def get_partner_focal_points(self, record: PartnersIntervention, values: dict, **kwargs):
        data = []
        ret = []
        for member in record.partner_focal_points.all():
            # member is AUTH_USER_MODEL
            ret.append("{0.last_name} {0.first_name} ({0.email}) {0.profile.phone_number}".format(member))
            data.append(
                dict(
                    last_name=member.last_name,
                    first_name=member.first_name,
                    email=member.email,
                    phone=member.profile.phone_number,
                )
            )

        values["partner_focal_points_data"] = data
        return ", ".join(ret)

    def get_fr_number(self, record: PartnersIntervention, values: dict, **kwargs):
        return ", ".join(
            FundsFundsreservationheader.objects.filter(intervention=record).values_list("fr_number", flat=True)
        )

    def get_outstanding_amt_local(self, record: PartnersIntervention, values: dict, **kwargs):
        return FundsFundsreservationheader.objects.filter(intervention=record).aggregate(Sum("outstanding_amt_local"))[
            "outstanding_amt_local__sum"
        ]

    def get_cp_outputs(self, record: PartnersIntervention, values: dict, **kwargs):
        values["cp_outputs_data"] = list(record.result_links.values("name", "wbs"))
        return ", ".join([rl.name for rl in record.result_links.all()])

    def get_unicef_focal_points(self, record: PartnersIntervention, values: dict, **kwargs):
        data = []
        ret = []
        for member in record.unicef_focal_points.all():
            ret.append("{0.last_name} {0.first_name} ({0.email})".format(member))
            data.append(
                dict(
                    last_name=member.last_name,
                    first_name=member.first_name,
                    email=member.email,
                )
            )

        values["unicef_focal_points_data"] = data
        return ", ".join(ret)

    def get_prc_review_document(self, record: PartnersIntervention, values: dict, **kwargs):
        from etools_datamart.apps.mart.data.models import Attachment

        attachment = (
            Attachment.objects.filter(
                # object_id=record.pk,
                pd_ssfa_number__in=[record.number, record.number[:-2] if record.number else ""],
                code="partners_intervention_prc_review",
                content_type=self._ct,
            )
            .order_by("-id")
            .first()
        )
        if attachment:
            return attachment.file

    def get_final_partnership_review(self, record: PartnersIntervention, values: dict, **kwargs):
        from etools_datamart.apps.mart.data.models import Attachment

        attachment = Attachment.objects.filter(
            pd_ssfa_number=record.number, code="partners_intervention_attachment", content_type="interventionattachment"
        ).last()
        if attachment:
            return attachment.file


class Intervention(NestedLocationMixin, InterventionAbstract, EtoolsDataMartModel):
    final_partnership_review = models.CharField(max_length=1024, null=True)

    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True, default=dict)

    loader = InterventionLoader()

    class Meta:
        ordering = ("country_name", "title", "id")
        verbose_name = "Intervention"
        unique_together = ("schema_name", "intervention_id")

    class Options(InterventionAbstract.Options):
        mapping = dict(
            **InterventionAbstract.Options.mapping,
            locations_data="i",
            locations="-",
            final_partnership_review="-",
        )


class InterventionByLocationLoader(InterventionLoader):
    def get_values(self, record):
        values = super().get_values(record)
        values["location"] = Location.objects.filter(
            schema_name=self.context["country"].schema_name, source_id=record.location.id
        ).first()
        return values

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = self.filter_queryset(self.get_queryset().prefetch_related("flat_locations"))

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for intervention in page.object_list:
                for location in intervention.flat_locations.all():
                    intervention.location = location
                    filters = self.config.key(self, intervention)
                    values = self.get_values(intervention)
                    op = self.process_record(filters, values)
                    self.increment_counter(op)


class InterventionByLocation(LocationMixin, InterventionAbstract, EtoolsDataMartModel):
    loader = InterventionByLocationLoader()

    class Meta:
        ordering = ("country_name", "title")
        verbose_name = "Intervention By Location"
        unique_together = ("schema_name", "intervention_id", "location_source_id")

    class Options(InterventionAbstract.Options):
        key = lambda loader, record: dict(
            schema_name=loader.context["country"].schema_name,
            intervention_id=record.pk,
            location_source_id=record.location.pk,
        )
        mapping = add_location_mapping(InterventionAbstract.Options.mapping)
