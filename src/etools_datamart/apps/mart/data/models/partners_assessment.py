from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Partner
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import PartnersAssessment


class Assessment(EtoolsDataMartModel):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    type = models.CharField(max_length=50, blank=True, null=True)
    names_of_other_agencies = models.CharField(max_length=255, blank=True, null=True)

    partner_name = models.CharField(max_length=300, blank=True, null=True)
    vendor_number = models.CharField(max_length=30, blank=True, null=True)

    expected_budget = models.IntegerField(blank=True, null=True)
    requested_date = models.DateField()
    planned_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    rating = models.CharField(max_length=50, blank=True, null=True)
    report = models.CharField(max_length=1024, blank=True, null=True)
    current = models.BooleanField(blank=True, null=True)

    approving_officer = models.CharField(max_length=200, blank=True, null=True)
    requesting_officer = models.CharField(max_length=200, blank=True, null=True)

    active = models.BooleanField(default=True)

    loader = EtoolsLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = PartnersAssessment
        queryset = lambda: PartnersAssessment.objects.select_related(
            "partner", "partner__organization", "approving_officer", "requesting_officer"
        )
        depends = (Partner,)
        mapping = dict(
            partner_name="partner.organization.name",
            vendor_number="partner.organization.vendor_number",
            approving_officer="approving_officer.get_display_name",
            requesting_officer="requesting_officer.get_display_name",
        )
