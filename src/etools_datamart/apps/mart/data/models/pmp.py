import logging
from decimal import Decimal

from django.conf import settings
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce

from etools_datamart.apps.etl.paginator import DatamartPaginator
from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import PartnersIntervention, PartnersPartnerorganization

logger = logging.getLogger(__name__)


class PMPIndicatorLoader(EtoolsLoader):
    def get_queryset(self):
        return PartnersPartnerorganization.objects.all()

    def process_country(self):
        country = self.context["country"]

        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = self.get_queryset()

        paginator = DatamartPaginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for partner in page.object_list:
                for intervention in PartnersIntervention.objects.filter(agreement__partner=partner):
                    planned_budget = getattr(
                        intervention, "partnersintervention_partners_interventionbudget_intervention_id", None
                    )
                    fr_currencies = (
                        intervention.FundsFundsreservationheader_intervention.all()
                        .values_list(
                            "currency",
                            flat=True,
                        )
                        .distinct()
                    )
                    has_assessment = bool(getattr(partner.current_core_value_assessment, "assessment", False))
                    values = {
                        "country_name": country.name,
                        "schema_name": country.schema_name,
                        "area_code": country.business_area_code,
                        "partner_name": partner.organization.name,
                        "partner_type": partner.organization.cso_type,
                        "vendor_number": partner.organization.vendor_number,
                        "pd_ssfa_ref": intervention.number.replace(",", "-") if intervention.number else "-",
                        "pd_ssfa_status": intervention.status.lower(),
                        "pd_ssfa_start_date": intervention.start,
                        "pd_ssfa_creation_date": intervention.created,
                        "pd_ssfa_end_date": intervention.end,
                        "cash_contribution": intervention.total_unicef_cash or 0,
                        "supply_contribution": intervention.total_in_kind_amount or 0,
                        "total_budget": intervention.total_budget or 0,
                        "unicef_budget": intervention.total_unicef_budget or 0,
                        "currency": (
                            intervention.PartnersInterventionbudget_intervention.currency if planned_budget else "-"
                        ),
                        "partner_contribution": (
                            intervention.PartnersInterventionbudget_intervention.partner_contribution
                            if planned_budget
                            else "-"
                        ),
                        "unicef_cash": (
                            intervention.PartnersInterventionbudget_intervention.unicef_cash if planned_budget else "-"
                        ),
                        "in_kind_amount": (
                            intervention.PartnersInterventionbudget_intervention.in_kind_amount
                            if planned_budget
                            else "-"
                        ),
                        "total": intervention.PartnersInterventionbudget_intervention.total if planned_budget else "-",
                        "fr_numbers_against_pd_ssfa": " - ".join(
                            [fh.fr_number for fh in intervention.FundsFundsreservationheader_intervention.all()]
                        ),
                        "fr_currencies": ", ".join(fr for fr in fr_currencies),
                        "sum_of_all_fr_planned_amount": (
                            intervention.FundsFundsreservationheader_intervention.aggregate(
                                total=Coalesce(Sum("intervention_amt"), Decimal(0.0))
                            )["total"]
                            if fr_currencies.count() <= 1
                            else "-"
                        ),
                        "core_value_attached": has_assessment,
                        # 'partner_link': '{}/pmp/partners/{}/details'.format(base_url, partner.pk),
                        # 'intervention_link': '{}/pmp/interventions/{}/details'.format(base_url, intervention.pk),
                        "seen": self.context["today"],
                    }
                    op = self.process_record(
                        filters=dict(
                            country_name=country.name,
                            schema_name=country.schema_name,
                            partner_id=partner.pk,
                            intervention_id=intervention.pk,
                        ),
                        values=values,
                    )
                    self.increment_counter(op)


class PMPIndicators(EtoolsDataMartModel):
    vendor_number = models.CharField(max_length=255, null=True, db_index=True)

    partner_name = models.CharField(max_length=255, null=True, db_index=True)
    partner_type = models.CharField(max_length=255, null=True, db_index=True)
    pd_ssfa_ref = models.CharField(max_length=255, null=True)
    pd_ssfa_status = models.CharField(max_length=50, null=True, db_index=True)
    pd_ssfa_start_date = models.DateField(
        null=True,
    )
    pd_ssfa_creation_date = models.DateField(
        null=True,
    )
    pd_ssfa_end_date = models.DateField(
        null=True,
    )

    cash_contribution = models.DecimalField(
        max_digits=20, decimal_places=3, null=True, help_text="UNICEF US$ Cash contribution"
    )
    supply_contribution = models.DecimalField(
        max_digits=20, decimal_places=3, null=True, help_text="UNICEF US$ Supply contribution"
    )
    total_budget = models.DecimalField(
        max_digits=20, decimal_places=3, null=True, db_index=True, help_text="Total Budget"
    )
    unicef_budget = models.DecimalField(max_digits=20, decimal_places=3, null=True, help_text="UNICEF Budget")

    currency = models.CharField(max_length=201, null=True, help_text="Currency")
    partner_contribution = models.CharField(max_length=202, null=True, help_text="Partner Contribution")
    unicef_cash = models.CharField(max_length=203, null=True, help_text="Unicef Cash")
    in_kind_amount = models.CharField(max_length=204, null=True, help_text="In kind Amount")
    total = models.CharField(max_length=205, null=True, help_text="")
    fr_numbers_against_pd_ssfa = models.TextField(null=True, help_text="FR numbers against PD / SSFA")
    fr_currencies = models.CharField(max_length=207, null=True, help_text="FR currencies")
    sum_of_all_fr_planned_amount = models.CharField(max_length=208, null=True, help_text="Sum of all FR planned amount")
    core_value_attached = models.CharField(max_length=209, null=True, help_text="Core value attached")
    # partner_link = models.CharField(max_length=210, null=True, help_text='Partner Link')
    # intervention_link = models.CharField(max_length=211, null=True, help_text='Intervention Link')

    # country_id = models.IntegerField(null=True)
    partner_id = models.IntegerField(null=True)
    intervention_id = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(null=True)

    class Meta:
        ordering = ("country_name", "partner_name")
        verbose_name = "PMP Indicator"

    loader = PMPIndicatorLoader()

    class Options:
        source = PartnersPartnerorganization
        mapping = None
        sync_deleted_records = lambda loader: False
