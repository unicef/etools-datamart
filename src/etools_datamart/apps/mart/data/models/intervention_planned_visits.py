from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.mart.data.models.intervention import Intervention
from etools_datamart.apps.sources.etools.enrichment.consts import PartnersInterventionConst
from etools_datamart.apps.sources.etools.models import models, PartnersInterventionplannedvisits


class InterventionPlannedVisits(EtoolsDataMartModel):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    partner_vendor_number = models.CharField(max_length=100, blank=True, null=True)
    partner_name = models.CharField(max_length=200, null=True)
    pd_status = models.CharField(max_length=32, null=True, db_index=True, choices=PartnersInterventionConst.STATUSES)
    pd_reference_number = models.CharField(max_length=100, null=True)

    year = models.IntegerField()
    programmatic_q1 = models.IntegerField(default=0)
    programmatic_q2 = models.IntegerField(default=0)
    programmatic_q3 = models.IntegerField(default=0)
    programmatic_q4 = models.IntegerField(default=0)

    loader = EtoolsLoader()

    class Meta:
        ordering = ("-created",)
        verbose_name_plural = "Intervention Planned Visits"

    class Options:
        source = PartnersInterventionplannedvisits
        depends = (Intervention,)
        queryset = lambda: PartnersInterventionplannedvisits.objects.select_related(
            "intervention",
            "intervention__agreement",
            "intervention__agreement__partner",
        )
        key = lambda loader, record: dict(schema_name=loader.context["country"].schema_name, source_id=record.pk)
        mapping = dict(
            partner_vendor_number="intervention.agreement.partner.vendor_number",
            partner_name="intervention.agreement.partner.name",
            pd_status="intervention.status",
            pd_reference_number="intervention.reference_number",
            year="=",
            programmatic_q1="=",
            programmatic_q2="=",
            programmatic_q3="=",
            programmatic_q4="=",
        )
