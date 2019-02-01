# flake8: noqa F405.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class EquitrackDomain(models.Model):
    domain = models.CharField(unique=True, max_length=253)
    is_primary = models.BooleanField()
    tenant = models.ForeignKey('UsersCountry', models.DO_NOTHING, related_name='userscountry_EquiTrack_domain_tenant_id')

    class Meta:
        managed = False
        db_table = 'EquiTrack_domain'


class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254)
    verified = models.BooleanField()
    primary = models.BooleanField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='authuser_account_emailaddress_user_id')

    class Meta:
        managed = False
        db_table = 'account_emailaddress'


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING, related_name='accountemailaddress_account_emailconfirmation_email_address_id')

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, related_name='authgroup_auth_group_permissions_group_id')
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING, related_name='authpermission_auth_group_permissions_permission_id')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='djangocontenttype_auth_permission_content_type_id')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('codename', 'content_type'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(unique=True, max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    middle_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, related_name='authgroup_auth_user_groups_group_id')

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('group', 'user_id'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='authuser_auth_user_user_permissions_user_id')
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING, related_name='authpermission_auth_user_user_permissions_permission_id')

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('permission', 'user'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class CategoriesCategory(models.Model):
    order = models.IntegerField()
    module = models.CharField(max_length=10)
    description = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'categories_category'
        unique_together = (('description', 'module'),)


class CorsheadersCorsmodel(models.Model):
    cors = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'corsheaders_corsmodel'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='djangocontenttype_django_admin_log_content_type_id', blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='authuser_django_admin_log_user_id')

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCeleryBeatCrontabschedule(models.Model):
    minute = models.CharField(max_length=240)
    hour = models.CharField(max_length=96)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=124)
    month_of_year = models.CharField(max_length=64)
    timezone = models.CharField(max_length=63)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_crontabschedule'


class DjangoCeleryBeatIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_intervalschedule'


class DjangoCeleryBeatPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.BooleanField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.IntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    crontab = models.ForeignKey(DjangoCeleryBeatCrontabschedule, models.DO_NOTHING, related_name='djangocelerybeatcrontabschedule_django_celery_beat_periodictask_crontab_id', blank=True, null=True)
    interval = models.ForeignKey(DjangoCeleryBeatIntervalschedule, models.DO_NOTHING, related_name='djangocelerybeatintervalschedule_django_celery_beat_periodictask_interval_id', blank=True, null=True)
    solar = models.ForeignKey('DjangoCeleryBeatSolarschedule', models.DO_NOTHING, related_name='djangocelerybeatsolarschedule_django_celery_beat_periodictask_solar_id', blank=True, null=True)
    one_off = models.BooleanField()
    start_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictask'


class DjangoCeleryBeatPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictasks'


class DjangoCeleryBeatSolarschedule(models.Model):
    event = models.CharField(max_length=24)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_solarschedule'
        unique_together = (('event', 'latitude', 'longitude'),)


class DjangoCeleryResultsTaskresult(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    hidden = models.BooleanField()
    meta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_taskresult'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class DrfpasswordlessCallbacktoken(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
    is_active = models.BooleanField()
    to_alias = models.CharField(max_length=40)
    to_alias_type = models.CharField(max_length=20)
    key = models.CharField(unique=True, max_length=6)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='authuser_drfpasswordless_callbacktoken_user_id')

    class Meta:
        managed = False
        db_table = 'drfpasswordless_callbacktoken'
        unique_together = (('is_active', 'key'),)


class EasyThumbnailsSource(models.Model):
    storage_hash = models.CharField(max_length=40)
    name = models.CharField(max_length=255)
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'easy_thumbnails_source'
        unique_together = (('name', 'storage_hash'),)


class EasyThumbnailsThumbnail(models.Model):
    storage_hash = models.CharField(max_length=40)
    name = models.CharField(max_length=255)
    modified = models.DateTimeField()
    source = models.ForeignKey(EasyThumbnailsSource, models.DO_NOTHING, related_name='easythumbnailssource_easy_thumbnails_thumbnail_source_id')

    class Meta:
        managed = False
        db_table = 'easy_thumbnails_thumbnail'
        unique_together = (('name', 'source', 'storage_hash'),)


class EasyThumbnailsThumbnaildimensions(models.Model):
    thumbnail = models.OneToOneField(EasyThumbnailsThumbnail, models.DO_NOTHING, related_name='easythumbnailsthumbnail_easy_thumbnails_thumbnaildimensions_thumbnail_id')
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'easy_thumbnails_thumbnaildimensions'


class EnvironmentIssuecheckconfig(models.Model):
    check_id = models.CharField(unique=True, max_length=100)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'environment_issuecheckconfig'


class EnvironmentTenantflag(models.Model):
    authenticated = models.BooleanField()
    created = models.DateTimeField()
    everyone = models.NullBooleanField()
    languages = models.TextField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=100)
    note = models.TextField()
    percent = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    rollout = models.BooleanField()
    staff = models.BooleanField()
    superusers = models.BooleanField()
    testing = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'environment_tenantflag'


class EnvironmentTenantflagCountries(models.Model):
    tenantflag = models.ForeignKey(EnvironmentTenantflag, models.DO_NOTHING, related_name='environmenttenantflag_environment_tenantflag_countries_tenantflag_id')
    country = models.ForeignKey('UsersCountry', models.DO_NOTHING, related_name='userscountry_environment_tenantflag_countries_country_id')

    class Meta:
        managed = False
        db_table = 'environment_tenantflag_countries'
        unique_together = (('country', 'tenantflag'),)


class EnvironmentTenantflagGroups(models.Model):
    tenantflag = models.ForeignKey(EnvironmentTenantflag, models.DO_NOTHING, related_name='environmenttenantflag_environment_tenantflag_groups_tenantflag_id')
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, related_name='authgroup_environment_tenantflag_groups_group_id')

    class Meta:
        managed = False
        db_table = 'environment_tenantflag_groups'
        unique_together = (('group', 'tenantflag'),)


class EnvironmentTenantflagUsers(models.Model):
    tenantflag = models.ForeignKey(EnvironmentTenantflag, models.DO_NOTHING, related_name='environmenttenantflag_environment_tenantflag_users_tenantflag_id')
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='authuser_environment_tenantflag_users_user_id')

    class Meta:
        managed = False
        db_table = 'environment_tenantflag_users'
        unique_together = (('tenantflag', 'user'),)


class EnvironmentTenantswitch(models.Model):
    active = models.BooleanField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=100)
    note = models.TextField()

    class Meta:
        managed = False
        db_table = 'environment_tenantswitch'


class EnvironmentTenantswitchCountries(models.Model):
    tenantswitch = models.ForeignKey(EnvironmentTenantswitch, models.DO_NOTHING, related_name='environmenttenantswitch_environment_tenantswitch_countries_tenantswitch_id')
    country = models.ForeignKey('UsersCountry', models.DO_NOTHING, related_name='userscountry_environment_tenantswitch_countries_country_id')

    class Meta:
        managed = False
        db_table = 'environment_tenantswitch_countries'
        unique_together = (('country', 'tenantswitch'),)


class GenericLinksGenericlink(models.Model):
    content_type_id = models.IntegerField()
    object_id = models.IntegerField()
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    is_external = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'generic_links_genericlink'


class NotificationNotification(models.Model):
    type = models.CharField(max_length=255)
    object_id = models.IntegerField(blank=True, null=True)
    recipients = models.TextField()  # This field type is a guess.
    sent_recipients = models.TextField()  # This field type is a guess.
    template_name = models.CharField(max_length=255)
    template_data = models.TextField(blank=True, null=True)  # This field type is a guess.
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, related_name='djangocontenttype_notification_notification_content_type_id', blank=True, null=True)
    cc = models.TextField()  # This field type is a guess.
    from_address = models.CharField(max_length=255, blank=True, null=True)
    html_message = models.TextField()
    sent_email = models.ForeignKey('PostOfficeEmail', models.DO_NOTHING, related_name='postofficeemail_notification_notification_sent_email_id', blank=True, null=True)
    subject = models.TextField()
    text_message = models.TextField()

    class Meta:
        managed = False
        db_table = 'notification_notification'


class Permissions2Permission(models.Model):
    permission = models.CharField(max_length=10)
    permission_type = models.CharField(max_length=10)
    target = models.CharField(max_length=100)
    condition = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'permissions2_permission'


class PostOfficeAttachment(models.Model):
    file = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'post_office_attachment'


class PostOfficeAttachmentEmails(models.Model):
    attachment = models.ForeignKey(PostOfficeAttachment, models.DO_NOTHING, related_name='postofficeattachment_post_office_attachment_emails_attachment_id')
    email = models.ForeignKey('PostOfficeEmail', models.DO_NOTHING, related_name='postofficeemail_post_office_attachment_emails_email_id')

    class Meta:
        managed = False
        db_table = 'post_office_attachment_emails'
        unique_together = (('attachment', 'email'),)


class PostOfficeEmail(models.Model):
    from_email = models.CharField(max_length=254)
    to = models.TextField()
    cc = models.TextField()
    bcc = models.TextField()
    subject = models.CharField(max_length=989)
    message = models.TextField()
    html_message = models.TextField()
    status = models.SmallIntegerField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    created = models.DateTimeField()
    last_updated = models.DateTimeField()
    scheduled_time = models.DateTimeField(blank=True, null=True)
    headers = models.TextField(blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    template = models.ForeignKey('PostOfficeEmailtemplate', models.DO_NOTHING, related_name='postofficeemailtemplate_post_office_email_template_id', blank=True, null=True)
    backend_alias = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'post_office_email'


class PostOfficeEmailtemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.CharField(max_length=255)
    content = models.TextField()
    html_content = models.TextField()
    created = models.DateTimeField()
    last_updated = models.DateTimeField()
    default_template = models.ForeignKey('self', models.DO_NOTHING, related_name='postofficeemailtemplate_post_office_emailtemplate_default_template_id', blank=True, null=True)
    language = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'post_office_emailtemplate'
        unique_together = (('default_template', 'language', 'name'),)


class PostOfficeLog(models.Model):
    date = models.DateTimeField()
    status = models.SmallIntegerField()
    exception_type = models.CharField(max_length=255)
    message = models.TextField()
    email = models.ForeignKey(PostOfficeEmail, models.DO_NOTHING, related_name='postofficeemail_post_office_log_email_id')

    class Meta:
        managed = False
        db_table = 'post_office_log'


class PublicsAirlinecompany(models.Model):
    name = models.CharField(max_length=255)
    code = models.IntegerField()
    iata = models.CharField(max_length=3)
    icao = models.CharField(max_length=3)
    country = models.CharField(max_length=255)
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'publics_airlinecompany'


class PublicsBusinessarea(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=32)
    region = models.ForeignKey('PublicsBusinessregion', models.DO_NOTHING, related_name='publicsbusinessregion_publics_businessarea_region_id')
    default_currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, related_name='publicscurrency_publics_businessarea_default_currency_id', blank=True, null=True)
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'publics_businessarea'


class PublicsBusinessregion(models.Model):
    name = models.CharField(max_length=16)
    code = models.CharField(max_length=2)
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'publics_businessregion'


class PublicsCountry(models.Model):
    name = models.CharField(max_length=64)
    long_name = models.CharField(max_length=128)
    vision_code = models.CharField(unique=True, max_length=3, blank=True, null=True)
    iso_2 = models.CharField(max_length=2)
    iso_3 = models.CharField(max_length=3)
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    business_area = models.ForeignKey(PublicsBusinessarea, models.DO_NOTHING, related_name='publicsbusinessarea_publics_country_business_area_id', blank=True, null=True)
    currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, related_name='publicscurrency_publics_country_currency_id', blank=True, null=True)
    deleted_at = models.DateTimeField()
    dsa_code = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'publics_country'


class PublicsCurrency(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=5)
    decimal_places = models.IntegerField()
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'publics_currency'


class PublicsDsarate(models.Model):
    effective_to_date = models.DateField()
    dsa_amount_usd = models.DecimalField(max_digits=20, decimal_places=4)
    dsa_amount_60plus_usd = models.DecimalField(max_digits=20, decimal_places=4)
    dsa_amount_local = models.DecimalField(max_digits=20, decimal_places=4)
    dsa_amount_60plus_local = models.DecimalField(max_digits=20, decimal_places=4)
    room_rate = models.DecimalField(max_digits=20, decimal_places=4)
    finalization_date = models.DateField()
    effective_from_date = models.DateField()
    region = models.ForeignKey('PublicsDsaregion', models.DO_NOTHING, related_name='publicsdsaregion_publics_dsarate_region_id')

    class Meta:
        managed = False
        db_table = 'publics_dsarate'
        unique_together = (('effective_to_date', 'region'),)


class PublicsDsarateupload(models.Model):
    dsa_file = models.CharField(max_length=100)
    status = models.CharField(max_length=64)
    upload_date = models.DateTimeField()
    errors = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'publics_dsarateupload'


class PublicsDsaregion(models.Model):
    area_name = models.CharField(max_length=120)
    area_code = models.CharField(max_length=3)
    country = models.ForeignKey(PublicsCountry, models.DO_NOTHING, related_name='publicscountry_publics_dsaregion_country_id')
    deleted_at = models.DateTimeField()
    user_defined = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'publics_dsaregion'


class PublicsExchangerate(models.Model):
    valid_from = models.DateField()
    valid_to = models.DateField()
    x_rate = models.DecimalField(max_digits=10, decimal_places=5)
    currency = models.ForeignKey(PublicsCurrency, models.DO_NOTHING, related_name='publicscurrency_publics_exchangerate_currency_id')
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'publics_exchangerate'


class PublicsFund(models.Model):
    name = models.CharField(max_length=25)
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'publics_fund'


class PublicsGrant(models.Model):
    name = models.CharField(max_length=25)
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'publics_grant'


class PublicsGrantFunds(models.Model):
    grant = models.ForeignKey(PublicsGrant, models.DO_NOTHING, related_name='publicsgrant_publics_grant_funds_grant_id')
    fund = models.ForeignKey(PublicsFund, models.DO_NOTHING, related_name='publicsfund_publics_grant_funds_fund_id')

    class Meta:
        managed = False
        db_table = 'publics_grant_funds'
        unique_together = (('fund', 'grant'),)


class PublicsTravelagent(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    country = models.ForeignKey(PublicsCountry, models.DO_NOTHING, related_name='publicscountry_publics_travelagent_country_id')
    expense_type = models.OneToOneField('PublicsTravelexpensetype', models.DO_NOTHING, related_name='publicstravelexpensetype_publics_travelagent_expense_type_id')
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'publics_travelagent'


class PublicsTravelexpensetype(models.Model):
    title = models.CharField(max_length=128)
    vendor_number = models.CharField(max_length=128)
    rank = models.IntegerField()
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'publics_travelexpensetype'


class PublicsWbs(models.Model):
    name = models.CharField(max_length=25)
    business_area = models.ForeignKey(PublicsBusinessarea, models.DO_NOTHING, related_name='publicsbusinessarea_publics_wbs_business_area_id', blank=True, null=True)
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'publics_wbs'


class PublicsWbsGrants(models.Model):
    wbs = models.ForeignKey(PublicsWbs, models.DO_NOTHING, related_name='publicswbs_publics_wbs_grants_wbs_id')
    grant = models.ForeignKey(PublicsGrant, models.DO_NOTHING, related_name='publicsgrant_publics_wbs_grants_grant_id')

    class Meta:
        managed = False
        db_table = 'publics_wbs_grants'
        unique_together = (('grant', 'wbs'),)


class PurchaseOrderAuditorfirm(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    vendor_number = models.CharField(unique=True, max_length=30)
    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=500)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=32)
    country = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=32)
    blocked = models.BooleanField()
    hidden = models.BooleanField()
    deleted_flag = models.BooleanField()
    vision_synced = models.BooleanField()
    unicef_users_allowed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'purchase_order_auditorfirm'


class PurchaseOrderAuditorstaffmember(models.Model):
    auditor_firm = models.ForeignKey(PurchaseOrderAuditorfirm, models.DO_NOTHING, related_name='purchaseorderauditorfirm_purchase_order_auditorstaffmember_auditor_firm_id')
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, related_name='authuser_purchase_order_auditorstaffmember_user_id')
    hidden = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'purchase_order_auditorstaffmember'


class PurchaseOrderPurchaseorder(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    order_number = models.CharField(unique=True, max_length=30, blank=True, null=True)
    contract_start_date = models.DateField(blank=True, null=True)
    contract_end_date = models.DateField(blank=True, null=True)
    auditor_firm = models.ForeignKey(PurchaseOrderAuditorfirm, models.DO_NOTHING, related_name='purchaseorderauditorfirm_purchase_order_purchaseorder_auditor_firm_id')

    class Meta:
        managed = False
        db_table = 'purchase_order_purchaseorder'


class PurchaseOrderPurchaseorderitem(models.Model):
    number = models.IntegerField()
    purchase_order = models.ForeignKey(PurchaseOrderPurchaseorder, models.DO_NOTHING, related_name='purchaseorderpurchaseorder_purchase_order_purchaseorderitem_purchase_order_id')

    class Meta:
        managed = False
        db_table = 'purchase_order_purchaseorderitem'
        unique_together = (('number', 'purchase_order'),)


class RegistrationRegistrationprofile(models.Model):
    user_id = models.IntegerField(unique=True)
    activation_key = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'registration_registrationprofile'


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=30)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    extra_data = models.TextField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING, related_name='socialaccountsocialapp_socialaccount_socialapp_sites_socialapp_id')
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING, related_name='djangosite_socialaccount_socialapp_sites_site_id')

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('site', 'socialapp'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING, related_name='socialaccountsocialaccount_socialaccount_socialtoken_account_id')
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING, related_name='socialaccountsocialapp_socialaccount_socialtoken_app_id')

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('account', 'app'),)


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class TpmpartnersTpmpartner(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    vendor_number = models.CharField(unique=True, max_length=30)
    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=500)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=32)
    country = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=32)
    vision_synced = models.BooleanField()
    blocked = models.BooleanField()
    hidden = models.BooleanField()
    deleted_flag = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tpmpartners_tpmpartner'


class TpmpartnersTpmpartnerCountries(models.Model):
    tpmpartner = models.ForeignKey(TpmpartnersTpmpartner, models.DO_NOTHING, related_name='tpmpartnerstpmpartner_tpmpartners_tpmpartner_countries_tpmpartner_id')
    country = models.ForeignKey('UsersCountry', models.DO_NOTHING, related_name='userscountry_tpmpartners_tpmpartner_countries_country_id')

    class Meta:
        managed = False
        db_table = 'tpmpartners_tpmpartner_countries'
        unique_together = (('country', 'tpmpartner'),)


class TpmpartnersTpmpartnerstaffmember(models.Model):
    receive_tpm_notifications = models.BooleanField()
    tpm_partner = models.ForeignKey(TpmpartnersTpmpartner, models.DO_NOTHING, related_name='tpmpartnerstpmpartner_tpmpartners_tpmpartnerstaffmember_tpm_partner_id')
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, related_name='authuser_tpmpartners_tpmpartnerstaffmember_user_id')

    class Meta:
        managed = False
        db_table = 'tpmpartners_tpmpartnerstaffmember'


class UnicefNotificationNotification(models.Model):
    method_type = models.CharField(max_length=255)
    object_id = models.IntegerField(blank=True, null=True)
    from_address = models.CharField(max_length=255, blank=True, null=True)
    recipients = models.TextField()  # This field type is a guess.
    cc = models.TextField()  # This field type is a guess.
    sent_recipients = models.TextField()  # This field type is a guess.
    template_name = models.CharField(max_length=255)
    template_data = models.TextField(blank=True, null=True)  # This field type is a guess.
    subject = models.TextField()
    text_message = models.TextField()
    html_message = models.TextField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, related_name='djangocontenttype_unicef_notification_notification_content_type_id', blank=True, null=True)
    sent_email = models.ForeignKey(PostOfficeEmail, models.DO_NOTHING, related_name='postofficeemail_unicef_notification_notification_sent_email_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_notification_notification'


class UsersCountry(models.Model):
    schema_name = models.CharField(unique=True, max_length=63)
    name = models.CharField(max_length=100)
    business_area_code = models.CharField(max_length=10)
    initial_zoom = models.IntegerField()
    latitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    country_short_code = models.CharField(max_length=10)
    vision_sync_enabled = models.BooleanField()
    vision_last_synced = models.DateTimeField(blank=True, null=True)
    threshold_tae_usd = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    threshold_tre_usd = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    local_currency = models.ForeignKey(PublicsCurrency, models.DO_NOTHING, related_name='publicscurrency_users_country_local_currency_id', blank=True, null=True)
    long_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users_country'


class UsersCountryOffices(models.Model):
    country = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='userscountry_users_country_offices_country_id')
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='usersoffice_users_country_offices_office_id')

    class Meta:
        managed = False
        db_table = 'users_country_offices'
        unique_together = (('country', 'office'),)


class UsersOffice(models.Model):
    name = models.CharField(max_length=254)
    zonal_chief = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='authuser_users_office_zonal_chief_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_office'


class UsersUserprofile(models.Model):
    job_title = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='userscountry_users_userprofile_country_id', blank=True, null=True)
    office = models.ForeignKey(UsersOffice, models.DO_NOTHING, related_name='usersoffice_users_userprofile_office_id', blank=True, null=True)
    user_id = models.IntegerField(unique=True)
    country_override = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='userscountry_users_userprofile_country_override_id', blank=True, null=True)
    partner_staff_member = models.IntegerField(blank=True, null=True)
    guid = models.CharField(unique=True, max_length=40, blank=True, null=True)
    org_unit_code = models.CharField(max_length=32, blank=True, null=True)
    org_unit_name = models.CharField(max_length=64, blank=True, null=True)
    post_number = models.CharField(max_length=32, blank=True, null=True)
    post_title = models.CharField(max_length=64, blank=True, null=True)
    staff_id = models.CharField(max_length=32, blank=True, null=True)
    vendor_number = models.CharField(unique=True, max_length=32, blank=True, null=True)
    oic = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='authuser_users_userprofile_oic_id', blank=True, null=True)
    supervisor = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='authuser_users_userprofile_supervisor_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_userprofile'


class UsersUserprofileCountriesAvailable(models.Model):
    userprofile = models.ForeignKey(UsersUserprofile, models.DO_NOTHING, related_name='usersuserprofile_users_userprofile_countries_available_userprofile_id')
    country = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='userscountry_users_userprofile_countries_available_country_id')

    class Meta:
        managed = False
        db_table = 'users_userprofile_countries_available'
        unique_together = (('country', 'userprofile'),)


class UsersWorkspacecounter(models.Model):
    travel_reference_number_counter = models.IntegerField()
    travel_invoice_reference_number_counter = models.IntegerField()
    workspace = models.OneToOneField(UsersCountry, models.DO_NOTHING, related_name='userscountry_users_workspacecounter_workspace_id')

    class Meta:
        managed = False
        db_table = 'users_workspacecounter'


class VisionVisionsynclog(models.Model):
    handler_name = models.CharField(max_length=50)
    total_records = models.IntegerField()
    total_processed = models.IntegerField()
    successful = models.BooleanField()
    exception_message = models.TextField()
    date_processed = models.DateTimeField()
    country = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='userscountry_vision_visionsynclog_country_id')
    details = models.CharField(max_length=2048)

    class Meta:
        managed = False
        db_table = 'vision_visionsynclog'
