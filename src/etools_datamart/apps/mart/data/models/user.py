from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from etools_datamart.apps.mart.data.loader import CommonSchemaLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import AuthUser


class EtoolsUserLoader(CommonSchemaLoader):
    """
    --
    SELECT COUNT(*) AS "__count" FROM "auth_user";

    --
    SELECT "auth_user"."id",
           "auth_user"."password",
           "auth_user"."last_login",        -- mapped to .last_login
           "auth_user"."is_superuser",      -- mapped to .is_superuser
           "auth_user"."username",          -- mapped to .username
           "auth_user"."first_name",        -- mapped to .first_name
           "auth_user"."last_name",         -- mapped to .last_name
           "auth_user"."email",             -- mapped to .email
           "auth_user"."is_staff",          -- mapped to .is_staff
           "auth_user"."is_active",         -- mapped to .is_active
           "auth_user"."date_joined",       -- mapped to .date_joined
           "auth_user"."middle_name",       -- mapped to .middle_name
           "auth_user"."created",           -- mapped to .created
           "auth_user"."modified",          -- mapped to .modified
           "auth_user"."preferences"
    FROM "auth_user"
    ORDER BY "auth_user"."id" ASC
    LIMIT ##PAGE_SIZE## OFFSET ##PAGE_OFFSET##;

    --
    SELECT "users_userprofile"."id",
           "users_userprofile"."job_title",              -- mapped to .modified
           "users_userprofile"."phone_number",           -- mapped to .phone_number
           "users_userprofile"."country_id",
           "users_userprofile"."office_id",
           "users_userprofile"."country_override_id",
           "users_userprofile"."_partner_staff_member",  -- mapped to .partner_staff_member
           "users_userprofile"."guid",                   -- mapped to .guid
           "users_userprofile"."org_unit_code",          -- mapped to .org_unit_code
           "users_userprofile"."org_unit_name",          -- mapped to .org_unit_name
           "users_userprofile"."post_number",            -- mapped to .post_number
           "users_userprofile"."post_title",             -- mapped to .post_title
           "users_userprofile"."staff_id",               -- mapped to .staff_id
           "users_userprofile"."vendor_number",          -- mapped to .vendor_number
           "users_userprofile"."oic_id",                 -- mapped to .oic
           "users_userprofile"."supervisor_id",          -- mapped to .superviser
           "users_userprofile"."organization_id",
           "users_userprofile"."receive_tpm_notifications",
           "users_userprofile"."user_id"
    FROM "users_userprofile"
    WHERE "users_userprofile"."user_id"(##List of  "auth_user"."id" in the page ##);

    --
    SELECT "organizations_organization"."id",
           "organizations_organization"."created",
           "organizations_organization"."modified",
           "organizations_organization"."name",
           "organizations_organization"."vendor_number",
           "organizations_organization"."organization_type",
           "organizations_organization"."cso_type",
           "organizations_organization"."short_name",
           "organizations_organization"."other",
           "organizations_organization"."parent_id"
    FROM "organizations_organization"
    WHERE "organizations_organization"."id" in (## List of "users_userprofile"."organization_id" in the page##);

    --
    SELECT DISTINCT "auth_group"."name"
    FROM "users_realm"
    INNER JOIN "auth_group" ON ("users_realm"."group_id" = "auth_group"."id")
    WHERE "users_realm"."user_id" IN (## List of "auth_user"."id" in the page##);

    --
    SELECT DISTINCT "users_country"."name"              -- maps to .country_name
    FROM "users_realm"
    INNER JOIN "users_country" ON ("users_realm"."country_id" = "users_country"."id")
    WHERE "users_realm"."user_id" IN (## List of "auth_user"."id" in the page##);

    --
    SELECT "users_office"."id",
           "users_office"."name",                    -- mapped to .office
           "users_office"."zonal_chief_id"
    FROM "users_office"
    WHERE "users_office"."id" IN (## List of "users_userprofile"."office_id" in the page##);


    """

    ##  maps to .groups
    def get_groups(self, record, values, **kwargs):
        return ", ".join(record.UsersRealm_user.values_list("group__name", flat=True).distinct())

    ##  maps to .countries_available
    def get_countries_available(self, record, values, **kwargs):
        try:
            return ", ".join(record.UsersRealm_user.values_list("country__name", flat=True).distinct())
        except ObjectDoesNotExist:  # pragma: no cover
            return ""


class EtoolsUser(EtoolsDataMartModel):
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(unique=True, max_length=254)
    is_staff = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    job_title = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    partner_staff_member = models.IntegerField(blank=True, null=True)
    guid = models.CharField(unique=True, max_length=40, blank=True, null=True)
    org_unit_code = models.CharField(max_length=32, blank=True, null=True)
    org_unit_name = models.CharField(max_length=64, blank=True, null=True)
    post_number = models.CharField(max_length=32, blank=True, null=True)
    post_title = models.CharField(max_length=64, blank=True, null=True)
    staff_id = models.CharField(max_length=32, blank=True, null=True)
    vendor_number = models.CharField(max_length=32, blank=True, null=True)

    # country = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='userscountry_users_userprofile_country_id', blank=True, null=True)
    # office = models.ForeignKey(UsersOffice, models.DO_NOTHING, related_name='usersoffice_users_userprofile_office_id', blank=True, null=True)
    # country_override = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='userscountry_users_userprofile_country_override_id', blank=True, null=True)
    # oic = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='authuser_users_userprofile_oic_id', blank=True, null=True)
    # supervisor = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='authuser_users_userprofile_supervisor_id', blank=True, null=True)

    groups = models.TextField(blank=True, null=True)
    countries_available = models.TextField(blank=True, null=True)
    country_name = models.CharField(max_length=100, blank=True, null=True)
    country_override = models.CharField(max_length=100, blank=True, null=True)
    office = models.CharField(max_length=100, blank=True, null=True)
    supervisor = models.CharField(max_length=100, blank=True, null=True)
    oic = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ("email",)

    loader = EtoolsUserLoader()

    class Options:
        source = AuthUser
        sync_deleted_records = lambda loader: False
        truncate = True
        key = lambda loader, record: dict(source_id=record.id)

        mapping = dict(
            job_title="profile.job_title",
            phone_number="profile.phone_number",
            partner_staff_member="profile.partner_staff_member",
            guid="profile.guid",
            org_unit_code="profile.org_unit_code",
            org_unit_name="profile.org_unit_name",
            post_number="profile.post_number",
            post_title="profile.post_title",
            staff_id="profile.staff_id",
            vendor_number="profile.organization.vendor_number",
            country_name="profile.country.name",
            office="profile.office.name",
            country_override="i",
            oic="profile.oic.office",
            supervisor="profile.oic.office",
        )
