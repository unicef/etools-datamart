from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from etools_datamart.apps.mart.data.loader import CommonSchemaLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import AuthUser


class EtoolsUserLoader(CommonSchemaLoader):
    def get_groups(self, record, values, **kwargs):
        return ", ".join(record.groups.values_list("name", flat=True))

    def get_countries_available(self, record, values, **kwargs):
        try:
            return ", ".join(record.profile.countries_available.values_list("name", flat=True))
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
    vendor_number = models.CharField(unique=True, max_length=32, blank=True, null=True)

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
            vendor_number="profile.vendor_number",
            country_name="profile.country.name",
            office="profile.office.name",
            country_override="i",
            oic="profile.oic.office",
            supervisor="profile.oic.office",
        )
