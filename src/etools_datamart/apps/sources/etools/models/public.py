# flake8: noqa F405.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254)
    verified = models.BooleanField()
    primary = models.BooleanField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='AccountEmailaddress_user')

    class Meta:
        managed = False
        db_table = 'account_emailaddress'


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING, related_name='AccountEmailconfirmation_email_address')

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, related_name='AuthGroupPermissions_group')
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING, related_name='AuthGroupPermissions_permission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='AuthPermission_content_type')
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
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, related_name='AuthUserGroups_group')

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('group', 'user_id'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='AuthUserUserPermissions_user')
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING, related_name='AuthUserUserPermissions_permission')

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


class CoreDomain(models.Model):
    domain = models.CharField(unique=True, max_length=253)
    is_primary = models.BooleanField()
    tenant = models.ForeignKey('UsersCountry', models.DO_NOTHING, related_name='CoreDomain_tenant')

    class Meta:
        managed = False
        db_table = 'core_domain'


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
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='DjangoAdminLog_content_type', blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='DjangoAdminLog_user')

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCeleryBeatClockedschedule(models.Model):
    clocked_time = models.DateTimeField()
    enabled = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_clockedschedule'


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
    crontab = models.ForeignKey(DjangoCeleryBeatCrontabschedule, models.DO_NOTHING, related_name='DjangoCeleryBeatPeriodictask_crontab', blank=True, null=True)
    interval = models.ForeignKey(DjangoCeleryBeatIntervalschedule, models.DO_NOTHING, related_name='DjangoCeleryBeatPeriodictask_interval', blank=True, null=True)
    solar = models.ForeignKey('DjangoCeleryBeatSolarschedule', models.DO_NOTHING, related_name='DjangoCeleryBeatPeriodictask_solar', blank=True, null=True)
    one_off = models.BooleanField()
    start_time = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    headers = models.TextField()
    clocked = models.ForeignKey(DjangoCeleryBeatClockedschedule, models.DO_NOTHING, related_name='DjangoCeleryBeatPeriodictask_clocked', blank=True, null=True)

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
    task_args = models.TextField(blank=True, null=True)
    task_kwargs = models.TextField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)

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
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='DrfpasswordlessCallbacktoken_user')

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
    source = models.ForeignKey(EasyThumbnailsSource, models.DO_NOTHING, related_name='EasyThumbnailsThumbnail_source')

    class Meta:
        managed = False
        db_table = 'easy_thumbnails_thumbnail'
        unique_together = (('name', 'source', 'storage_hash'),)


class EasyThumbnailsThumbnaildimensions(models.Model):
    thumbnail = models.OneToOneField(EasyThumbnailsThumbnail, models.DO_NOTHING, related_name='EasyThumbnailsThumbnaildimensions_thumbnail')
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'easy_thumbnails_thumbnaildimensions'


class EnvironmentTenantflag(models.Model):
    authenticated = models.BooleanField()
    created = models.DateTimeField()
    everyone = models.BooleanField(null=True)
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
    tenantflag = models.ForeignKey(EnvironmentTenantflag, models.DO_NOTHING, related_name='EnvironmentTenantflagCountries_tenantflag')
    country = models.ForeignKey('UsersCountry', models.DO_NOTHING, related_name='EnvironmentTenantflagCountries_country')

    class Meta:
        managed = False
        db_table = 'environment_tenantflag_countries'
        unique_together = (('country', 'tenantflag'),)


class EnvironmentTenantflagGroups(models.Model):
    tenantflag = models.ForeignKey(EnvironmentTenantflag, models.DO_NOTHING, related_name='EnvironmentTenantflagGroups_tenantflag')
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, related_name='EnvironmentTenantflagGroups_group')

    class Meta:
        managed = False
        db_table = 'environment_tenantflag_groups'
        unique_together = (('group', 'tenantflag'),)


class EnvironmentTenantflagUsers(models.Model):
    tenantflag = models.ForeignKey(EnvironmentTenantflag, models.DO_NOTHING, related_name='EnvironmentTenantflagUsers_tenantflag')
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='EnvironmentTenantflagUsers_user')

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
    tenantswitch = models.ForeignKey(EnvironmentTenantswitch, models.DO_NOTHING, related_name='EnvironmentTenantswitchCountries_tenantswitch')
    country = models.ForeignKey('UsersCountry', models.DO_NOTHING, related_name='EnvironmentTenantswitchCountries_country')

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
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, related_name='NotificationNotification_content_type', blank=True, null=True)
    cc = models.TextField()  # This field type is a guess.
    from_address = models.CharField(max_length=255, blank=True, null=True)
    html_message = models.TextField()
    sent_email = models.ForeignKey('PostOfficeEmail', models.DO_NOTHING, related_name='NotificationNotification_sent_email', blank=True, null=True)
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
    headers = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_office_attachment'


class PostOfficeAttachmentEmails(models.Model):
    attachment = models.ForeignKey(PostOfficeAttachment, models.DO_NOTHING, related_name='PostOfficeAttachmentEmails_attachment')
    email = models.ForeignKey('PostOfficeEmail', models.DO_NOTHING, related_name='PostOfficeAttachmentEmails_email')

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
    template = models.ForeignKey('PostOfficeEmailtemplate', models.DO_NOTHING, related_name='PostOfficeEmail_template', blank=True, null=True)
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
    default_template = models.ForeignKey('self', models.DO_NOTHING, related_name='PostOfficeEmailtemplate_default_template', blank=True, null=True)
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
    email = models.ForeignKey(PostOfficeEmail, models.DO_NOTHING, related_name='PostOfficeLog_email')

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
    region = models.ForeignKey('PublicsBusinessregion', models.DO_NOTHING, related_name='PublicsBusinessarea_region')
    default_currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, related_name='PublicsBusinessarea_default_currency', blank=True, null=True)
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
    business_area = models.ForeignKey(PublicsBusinessarea, models.DO_NOTHING, related_name='PublicsCountry_business_area', blank=True, null=True)
    currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, related_name='PublicsCountry_currency', blank=True, null=True)
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
    region = models.ForeignKey('PublicsDsaregion', models.DO_NOTHING, related_name='PublicsDsarate_region')

    class Meta:
        managed = False
        db_table = 'publics_dsarate'
        unique_together = (('effective_to_date', 'region'),)


class PublicsDsaregion(models.Model):
    area_name = models.CharField(max_length=120)
    area_code = models.CharField(max_length=3)
    country = models.ForeignKey(PublicsCountry, models.DO_NOTHING, related_name='PublicsDsaregion_country')
    deleted_at = models.DateTimeField()
    user_defined = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'publics_dsaregion'


class PublicsExchangerate(models.Model):
    valid_from = models.DateField()
    valid_to = models.DateField()
    x_rate = models.DecimalField(max_digits=10, decimal_places=5)
    currency = models.ForeignKey(PublicsCurrency, models.DO_NOTHING, related_name='PublicsExchangerate_currency')
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'publics_exchangerate'


class PublicsTravelagent(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    country = models.ForeignKey(PublicsCountry, models.DO_NOTHING, related_name='PublicsTravelagent_country')
    expense_type = models.OneToOneField('PublicsTravelexpensetype', models.DO_NOTHING, related_name='PublicsTravelagent_expense_type')
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
    auditor_firm = models.ForeignKey(PurchaseOrderAuditorfirm, models.DO_NOTHING, related_name='PurchaseOrderAuditorstaffmember_auditor_firm')
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, related_name='PurchaseOrderAuditorstaffmember_user')
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
    auditor_firm = models.ForeignKey(PurchaseOrderAuditorfirm, models.DO_NOTHING, related_name='PurchaseOrderPurchaseorder_auditor_firm')

    class Meta:
        managed = False
        db_table = 'purchase_order_purchaseorder'


class PurchaseOrderPurchaseorderitem(models.Model):
    number = models.IntegerField()
    purchase_order = models.ForeignKey(PurchaseOrderPurchaseorder, models.DO_NOTHING, related_name='PurchaseOrderPurchaseorderitem_purchase_order')

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


class SocialAuthAssociation(models.Model):
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'social_auth_association'
        unique_together = (('handle', 'server_url'),)


class SocialAuthCode(models.Model):
    email = models.CharField(max_length=254)
    code = models.CharField(max_length=32)
    verified = models.BooleanField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_code'
        unique_together = (('code', 'email'),)


class SocialAuthNonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'social_auth_nonce'
        unique_together = (('salt', 'server_url', 'timestamp'),)


class SocialAuthPartial(models.Model):
    token = models.CharField(max_length=32)
    next_step = models.SmallIntegerField()
    backend = models.CharField(max_length=32)
    data = models.TextField()  # This field type is a guess.
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_partial'


class SocialAuthUsersocialauth(models.Model):
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = models.TextField()  # This field type is a guess.
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='SocialAuthUsersocialauth_user')

    class Meta:
        managed = False
        db_table = 'social_auth_usersocialauth'
        unique_together = (('provider', 'uid'),)


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
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING, related_name='SocialaccountSocialappSites_socialapp')
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING, related_name='SocialaccountSocialappSites_site')

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('site', 'socialapp'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING, related_name='SocialaccountSocialtoken_account')
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING, related_name='SocialaccountSocialtoken_app')

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
    tpmpartner = models.ForeignKey(TpmpartnersTpmpartner, models.DO_NOTHING, related_name='TpmpartnersTpmpartnerCountries_tpmpartner')
    country = models.ForeignKey('UsersCountry', models.DO_NOTHING, related_name='TpmpartnersTpmpartnerCountries_country')

    class Meta:
        managed = False
        db_table = 'tpmpartners_tpmpartner_countries'
        unique_together = (('country', 'tpmpartner'),)


class TpmpartnersTpmpartnerstaffmember(models.Model):
    receive_tpm_notifications = models.BooleanField()
    tpm_partner = models.ForeignKey(TpmpartnersTpmpartner, models.DO_NOTHING, related_name='TpmpartnersTpmpartnerstaffmember_tpm_partner')
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, related_name='TpmpartnersTpmpartnerstaffmember_user')

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
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, related_name='UnicefNotificationNotification_content_type', blank=True, null=True)
    sent_email = models.ForeignKey(PostOfficeEmail, models.DO_NOTHING, related_name='UnicefNotificationNotification_sent_email', blank=True, null=True)

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
    local_currency = models.ForeignKey(PublicsCurrency, models.DO_NOTHING, related_name='UsersCountry_local_currency', blank=True, null=True)
    long_name = models.CharField(max_length=255)
    iso3_code = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'users_country'


class UsersCountryOffices(models.Model):
    country = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='UsersCountryOffices_country')
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='UsersCountryOffices_office')

    class Meta:
        managed = False
        db_table = 'users_country_offices'
        unique_together = (('country', 'office'),)


class UsersOffice(models.Model):
    name = models.CharField(max_length=254)
    zonal_chief = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='UsersOffice_zonal_chief', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_office'


class UsersUserprofile(models.Model):
    job_title = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='UsersUserprofile_country', blank=True, null=True)
    office = models.ForeignKey(UsersOffice, models.DO_NOTHING, related_name='UsersUserprofile_office', blank=True, null=True)
    user_id = models.IntegerField(unique=True)
    country_override = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='UsersUserprofile_country_override', blank=True, null=True)
    field_partner_staff_member = models.IntegerField(db_column='_partner_staff_member', blank=True, null=True)  # Field renamed because it started with '_'.
    guid = models.CharField(unique=True, max_length=40, blank=True, null=True)
    org_unit_code = models.CharField(max_length=32, blank=True, null=True)
    org_unit_name = models.CharField(max_length=64, blank=True, null=True)
    post_number = models.CharField(max_length=32, blank=True, null=True)
    post_title = models.CharField(max_length=64, blank=True, null=True)
    staff_id = models.CharField(max_length=32, blank=True, null=True)
    vendor_number = models.CharField(unique=True, max_length=32, blank=True, null=True)
    oic = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='UsersUserprofile_oic', blank=True, null=True)
    supervisor = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='UsersUserprofile_supervisor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_userprofile'


class UsersUserprofileCountriesAvailable(models.Model):
    userprofile = models.ForeignKey(UsersUserprofile, models.DO_NOTHING, related_name='UsersUserprofileCountriesAvailable_userprofile')
    country = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='UsersUserprofileCountriesAvailable_country')

    class Meta:
        managed = False
        db_table = 'users_userprofile_countries_available'
        unique_together = (('country', 'userprofile'),)


class UsersWorkspacecounter(models.Model):
    travel_reference_number_counter = models.IntegerField()
    travel_invoice_reference_number_counter = models.IntegerField()
    workspace = models.OneToOneField(UsersCountry, models.DO_NOTHING, related_name='UsersWorkspacecounter_workspace')

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
    country = models.ForeignKey(UsersCountry, models.DO_NOTHING, related_name='VisionVisionsynclog_country')
    details = models.CharField(max_length=2048)
    business_area_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vision_visionsynclog'
