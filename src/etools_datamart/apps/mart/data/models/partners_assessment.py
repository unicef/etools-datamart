from django.db import models

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models import Partner
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import PartnersAssessment


class Assessment(EtoolsDataMartModel):
    """
    -- For each country;
    --
    SET search_path = public, a##COUNTRY##;

    --
    SELECT COUNT(*) AS "__count" FROM "partners_assessment";

    --
    SELECT '##COUNTRY##' AS __schema,
           "partners_assessment"."id",
           "partners_assessment"."type",
           "partners_assessment"."names_of_other_agencies",
           "partners_assessment"."expected_budget",
           "partners_assessment"."notes",
           "partners_assessment"."requested_date",
           "partners_assessment"."planned_date",
           "partners_assessment"."completed_date",
           "partners_assessment"."rating",
           "partners_assessment"."report",
           "partners_assessment"."current",
           "partners_assessment"."approving_officer_id",
           "partners_assessment"."partner_id",
           "partners_assessment"."requesting_officer_id",
           "partners_assessment"."created",
           "partners_assessment"."modified",
           "partners_assessment"."active",

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

           '##COUNTRY##' AS __schema,
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

           T5."id",
           T5."password",
           T5."last_login",
           T5."is_superuser",
           T5."username",
           T5."first_name",
           T5."last_name",
           T5."email",
           T5."is_staff",
           T5."is_active",
           T5."date_joined",
           T5."middle_name",
           T5."created",
           T5."modified",
           T5."preferences"
    FROM "partners_assessment" LEFT OUTER JOIN "auth_user" ON ("partners_assessment"."approving_officer_id" = "auth_user"."id")
    INNER JOIN "partners_partnerorganization" ON ("partners_assessment"."partner_id" = "partners_partnerorganization"."id")
    INNER JOIN "organizations_organization" ON ("partners_partnerorganization"."organization_id" = "organizations_organization"."id")
    LEFT OUTER JOIN "auth_user" T5 ON ("partners_assessment"."requesting_officer_id" = T5."id") ORDER BY "partners_assessment"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;
    """

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
