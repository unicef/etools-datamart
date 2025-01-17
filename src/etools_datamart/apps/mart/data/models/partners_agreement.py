from django.db import models
from django.db.models import JSONField, Prefetch

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import PartnersAgreementConst
from etools_datamart.apps.sources.etools.models import (
    AuthUser,
    PartnersAgreement,
    PartnersAgreementamendment,
    PartnersAgreementAuthorizedOfficers,
)


class AgreementLoader(EtoolsLoader):
    """
    --For each country;
    --
    SET search_path = public,##COUNTRY##;
    --
    SELECT COUNT(*) AS "__count" FROM "partners_agreement";

    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_agreement"."id",
           "partners_agreement"."created",
           "partners_agreement"."modified",
           "partners_agreement"."start",
           "partners_agreement"."end",
           "partners_agreement"."agreement_type",
           "partners_agreement"."agreement_number",
           "partners_agreement"."attached_agreement",
           "partners_agreement"."signed_by_unicef_date",
           "partners_agreement"."signed_by_partner_date",
           "partners_agreement"."partner_id",
           "partners_agreement"."signed_by_id",
           "partners_agreement"."status",
           "partners_agreement"."country_programme_id",
           "partners_agreement"."reference_number_year",
           "partners_agreement"."special_conditions_pca",
           "partners_agreement"."terms_acknowledged_by_id",
           "partners_agreement"."partner_manager_id",

           "partners_partnerorganization"."id",
           "partners_partnerorganization"."description",
           "partners_partnerorganization"."address",
           "partners_partnerorganization"."email",
           "partners_partnerorganization"."phone_number",
           "partners_partnerorganization"."alternate_id",
           "partners_partnerorganization"."alternate_name",
           "partners_partnerorganization"."rating",
           "partners_partnerorganization"."core_values_assessment_date",
           "partners_partnerorganization"."vision_synced",
           "partners_partnerorganization"."type_of_assessment",
           "partners_partnerorganization"."last_assessment_date",
           "partners_partnerorganization"."hidden",
           "partners_partnerorganization"."deleted_flag",
           "partners_partnerorganization"."total_ct_cp",
           "partners_partnerorganization"."total_ct_cy",
           "partners_partnerorganization"."blocked",
           "partners_partnerorganization"."city",
           "partners_partnerorganization"."country",
           "partners_partnerorganization"."postal_code",
           "partners_partnerorganization"."shared_with",
           "partners_partnerorganization"."street_address",
           "partners_partnerorganization"."hact_values",
           "partners_partnerorganization"."created",
           "partners_partnerorganization"."modified",
           "partners_partnerorganization"."net_ct_cy",
           "partners_partnerorganization"."reported_cy",
           "partners_partnerorganization"."total_ct_ytd",
           "partners_partnerorganization"."basis_for_risk_rating",
           "partners_partnerorganization"."manually_blocked",
           "partners_partnerorganization"."outstanding_dct_amount_6_to_9_months_usd",
           "partners_partnerorganization"."outstanding_dct_amount_more_than_9_months_usd",
           "partners_partnerorganization"."highest_risk_rating_name",
           "partners_partnerorganization"."highest_risk_rating_type",
           "partners_partnerorganization"."psea_assessment_date",
           "partners_partnerorganization"."sea_risk_rating_name",
           "partners_partnerorganization"."lead_office_id",
           "partners_partnerorganization"."lead_section_id",
           "partners_partnerorganization"."organization_id",

           "organizations_organization"."id",
           "organizations_organization"."created",
           "organizations_organization"."modified",
           "organizations_organization"."name",
           "organizations_organization"."vendor_number",
           "organizations_organization"."organization_type",
           "organizations_organization"."cso_type",
           "organizations_organization"."short_name",
           "organizations_organization"."other",
           "organizations_organization"."parent_id",

           "auth_user"."id",
           "auth_user"."password",
           "auth_user"."last_login",
           "auth_user"."is_superuser",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email",
           "auth_user"."is_staff",
           "auth_user"."is_active",
           "auth_user"."date_joined",
           "auth_user"."middle_name",
           "auth_user"."created",
           "auth_user"."modified",
           "auth_user"."preferences",

           "reports_countryprogramme"."id",
           "reports_countryprogramme"."name",
           "reports_countryprogramme"."wbs",
           "reports_countryprogramme"."from_date",
           "reports_countryprogramme"."to_date",
           "reports_countryprogramme"."invalid",

            T6."id",
            T6."password",
            T6."last_login",
            T6."is_superuser",
            T6."username",
            T6."first_name",
            T6."last_name",
            T6."email",
            T6."is_staff",
            T6."is_active",
            T6."date_joined",
            T6."middle_name",
            T6."created",
            T6."modified",
            T6."preferences",

            T7."id",
            T7."password",
            T7."last_login",
            T7."is_superuser",
            T7."username",
            T7."first_name",
            T7."last_name",
            T7."email",
            T7."is_staff",
            T7."is_active",
            T7."date_joined",
            T7."middle_name",
            T7."created",
            T7."modified",
            T7."preferences"
    FROM "partners_agreement" INNER JOIN "partners_partnerorganization" ON ("partners_agreement"."partner_id" = "partners_partnerorganization"."id")
    INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id")
    LEFT OUTER JOIN "auth_user" ON ("partners_agreement"."signed_by_id" = "auth_user"."id")
    LEFT OUTER JOIN "reports_countryprogramme" ON ("partners_agreement"."country_programme_id" = "reports_countryprogramme"."id")
    LEFT OUTER JOIN "auth_user" T6 ON ("partners_agreement"."terms_acknowledged_by_id" = T6."id")
    LEFT OUTER JOIN "auth_user" T7 ON ("partners_agreement"."partner_manager_id" = T7."id")
    ORDER BY "partners_agreement"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_agreementamendment"."id",
           "partners_agreementamendment"."created",
           "partners_agreementamendment"."modified",
           "partners_agreementamendment"."number",
           "partners_agreementamendment"."signed_amendment",
           "partners_agreementamendment"."signed_date",
           "partners_agreementamendment"."agreement_id",
           "partners_agreementamendment"."types"
    FROM "partners_agreementamendment"
    WHERE "partners_agreementamendment"."agreement_id" IN (##List of "partners_agreement"."id" in the page##);

    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_agreement_authorized_officers"."id",
           "partners_agreement_authorized_officers"."agreement_id",
           "partners_agreement_authorized_officers"."user_id"
    FROM "partners_agreement_authorized_officers"
    WHERE "partners_agreement_authorized_officers"."agreement_id" IN (##List of "partners_agreement"."id" in the page##);

    --
    SELECT "auth_user"."id",
           "auth_user"."password",
           "auth_user"."last_login",
           "auth_user"."is_superuser",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email",
           "auth_user"."is_staff",
           "auth_user"."is_active",
           "auth_user"."date_joined",
           "auth_user"."middle_name",
           "auth_user"."created",
           "auth_user"."modified",
           "auth_user"."preferences"
    FROM "auth_user"
    WHERE "auth_user"."id" IN (## List of "partners_agreement_authorized_officers"."user_id" in the page##);

    --
    SELECT "users_country"."id",
           "users_country"."schema_name",
           "users_country"."name",
           "users_country"."business_area_code",
           "users_country"."initial_zoom",
           "users_country"."latitude",
           "users_country"."longitude",
           "users_country"."country_short_code",
           "users_country"."vision_sync_enabled",
           "users_country"."vision_last_synced",
           "users_country"."local_currency_id",
           "users_country"."long_name",
           "users_country"."iso3_code",
           "users_country"."custom_dashboards"
    FROM "users_country"
    WHERE "users_country"."schema_name" = '##COUNTRY##';



    """

    def get_agreement_amendments(self, record: PartnersAgreement, values: dict, **kwargs):
        numbers = []
        for item in record.PartnersAgreementamendment_agreement.all():
            numbers.append(item.number)

        return ",".join(numbers)

    def get_partner_authorized_officers(self, record: PartnersAgreement, values: dict, **kwargs):
        officers = []
        for authorized in record.PartnersAgreementAuthorizedOfficers_agreement.all():
            officers.append(
                "%s %s (%s)" % (authorized.user.last_name, authorized.user.first_name, authorized.user.email)
            )
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
        queryset = (
            PartnersAgreement.objects.select_related(
                "partner__organization",
                "signed_by",
                "partner_manager",
                "terms_acknowledged_by",
                "country_programme",
            )
            .prefetch_related(
                Prefetch(
                    "PartnersAgreementamendment_agreement",
                    queryset=PartnersAgreementamendment.objects.all(),
                ),
                Prefetch(
                    "PartnersAgreementAuthorizedOfficers_agreement",
                    queryset=PartnersAgreementAuthorizedOfficers.objects.all(),
                ),
                Prefetch(
                    "PartnersAgreementAuthorizedOfficers_agreement__user",
                    queryset=AuthUser.objects.all(),
                ),
            )
            .all
            # TODO: Try getting only the required fields
        )

        mapping = {
            "partner_name": "partner.organization.name",
            "vendor_number": "partner.organization.vendor_number",
            "country_programme": "country_programme.name",
            "signed_by": "signed_by.name",
            "signed_by_partner": "partner_manager.name",
            "terms_acknowledged_by": "terms_acknowledged_by.name",
        }
