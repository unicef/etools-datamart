from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import PartnersAgreementConst
from etools_datamart.apps.sources.etools.models import PartnersAgreement


class AgreementLoader(EtoolsLoader):
    def get_agreement_amendments(self, record: PartnersAgreement, values: dict, **kwargs):
        return ",".join([a.number for a in record.amendments])

    def get_partner_authorized_officers(self, record: PartnersAgreement, values: dict, **kwargs):
        # PartnersPartnerstaffmember.objects.filter(agreement_authorizations=original)
        officers = []
        for authorized in record.authorized_officers.all():
            officers.append("%s %s (%s)" % (authorized.last_name, authorized.first_name, authorized.email))
        return ",".join(officers)


class Agreement(EtoolsDataMartModel):
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    agreement_type = models.CharField(
        max_length=10, choices=PartnersAgreementConst.AGREEMENT_TYPES, blank=True, null=True, db_index=True
    )
    agreement_number = models.CharField(max_length=45, blank=True, null=True)
    attached_agreement = models.CharField(max_length=1024, blank=True, null=True)
    signed_by_unicef_date = models.DateField(blank=True, null=True)
    signed_by_partner_date = models.DateField(blank=True, null=True)

    status = models.CharField(
        max_length=32, choices=PartnersAgreementConst.STATUS_CHOICES, db_index=True, blank=True, null=True
    )
    reference_number_year = models.IntegerField(blank=True, null=True)
    special_conditions_pca = models.BooleanField(blank=True, null=True)

    # partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='partnerspartnerorganization_partners_agreement_partner_id')
    # partner_manager = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, related_name='partnerspartnerstaffmember_partners_agreement_partner_manager_id', blank=True, null=True)
    # signed_by = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='authuser_partners_agreement_signed_by_id', blank=True, null=True)
    # country_programme = models.ForeignKey('ReportsCountryprogramme', models.DO_NOTHING, related_name='reportscountryprogramme_partners_agreement_country_programme_id', blank=True, null=True)

    partner_name = models.CharField(max_length=300, blank=True, null=True)
    country_programme = models.CharField(max_length=200, blank=True, null=True)
    signed_by = models.CharField(max_length=200, blank=True, null=True)

    reference_number = models.CharField(max_length=100, blank=True, null=True)
    vendor_number = models.CharField(max_length=100, blank=True, null=True)
    signed_by_partner = models.CharField(max_length=100, blank=True, null=True)
    partner_authorized_officers = models.TextField(blank=True, null=True)
    agreement_amendments = models.TextField(blank=True, null=True)
    terms_acknowledged_by = models.CharField(max_length=200, blank=True, null=True)

    loader = AgreementLoader()

    class Meta:
        unique_together = ("schema_name", "agreement_number")

    class Options:
        source = PartnersAgreement
        queryset = lambda: PartnersAgreement.objects.select_related(
            "partner__organization",
            "signed_by",
            "partner_manager",
            "terms_acknowledged_by",
        )
        mapping = {
            "partner_name": "partner.organization.name",
            "vendor_number": "partner.organization.vendor_number",
            "country_programme": "country_programme.name",
            "signed_by": "signed_by.name",
            "signed_by_partner": "partner_manager.name",
            "terms_acknowledged_by": "terms_acknowledged_by.name",
        }
