# flake8: noqa F405.
# This is an auto-generated PRP model module.
# Generated on 2019-12-13 11:17:44.226293
from django.contrib.gis.db import models

from etools_datamart.apps.core.readonly import ReadOnlyModel


class AccountUser(ReadOnlyModel):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    organization = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    partner = models.ForeignKey('source_prp.PartnerPartner', models.PROTECT, related_name='AccountUser_partner', blank=True, null=True)
    position = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_user'
        app_label = 'source_prp'


class AccountUserGroups(ReadOnlyModel):
    user = models.ForeignKey(AccountUser, models.PROTECT, related_name='AccountUserGroups_user')
    group = models.ForeignKey('source_prp.AuthGroup', models.PROTECT, related_name='AccountUserGroups_group')

    class Meta:
        managed = False
        db_table = 'account_user_groups'
        unique_together = (('user', 'group'),)
        app_label = 'source_prp'


class AccountUserprofile(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user = models.OneToOneField(AccountUser, models.PROTECT, related_name='AccountUserprofile_user')

    class Meta:
        managed = False
        db_table = 'account_userprofile'
        app_label = 'source_prp'


class AuthGroup(ReadOnlyModel):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'
        app_label = 'source_prp'


class AuthtokenToken(ReadOnlyModel):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AccountUser, models.PROTECT, related_name='AuthtokenToken_user')

    class Meta:
        managed = False
        db_table = 'authtoken_token'
        app_label = 'source_prp'


class ClusterCluster(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=32)
    imported_type = models.TextField(blank=True, null=True)
    response_plan = models.ForeignKey('source_prp.CoreResponseplan', models.PROTECT, related_name='ClusterCluster_response_plan', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cluster_cluster'
        unique_together = (('external_id', 'external_source'), ('type', 'imported_type', 'response_plan'),)
        app_label = 'source_prp'


class ClusterClusteractivity(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    title = models.TextField()
    cluster_objective = models.ForeignKey('source_prp.ClusterClusterobjective', models.PROTECT, related_name='ClusterClusteractivity_cluster_objective')

    class Meta:
        managed = False
        db_table = 'cluster_clusteractivity'
        unique_together = (('external_id', 'external_source'),)
        app_label = 'source_prp'


class ClusterClusteractivityLocations(ReadOnlyModel):
    clusteractivity = models.ForeignKey(ClusterClusteractivity, models.PROTECT, related_name='ClusterClusteractivityLocations_clusteractivity')
    location = models.ForeignKey('source_prp.CoreLocation', models.PROTECT, related_name='ClusterClusteractivityLocations_location')

    class Meta:
        managed = False
        db_table = 'cluster_clusteractivity_locations'
        unique_together = (('clusteractivity', 'location'),)
        app_label = 'source_prp'


class ClusterClusterobjective(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    title = models.TextField()
    cluster = models.ForeignKey(ClusterCluster, models.PROTECT, related_name='ClusterClusterobjective_cluster')

    class Meta:
        managed = False
        db_table = 'cluster_clusterobjective'
        unique_together = (('external_id', 'external_source'),)
        app_label = 'source_prp'


class ClusterClusterobjectiveLocations(ReadOnlyModel):
    clusterobjective = models.ForeignKey(ClusterClusterobjective, models.PROTECT, related_name='ClusterClusterobjectiveLocations_clusterobjective')
    location = models.ForeignKey('source_prp.CoreLocation', models.PROTECT, related_name='ClusterClusterobjectiveLocations_location')

    class Meta:
        managed = False
        db_table = 'cluster_clusterobjective_locations'
        unique_together = (('clusterobjective', 'location'),)
        app_label = 'source_prp'


class CoreCartodbtable(ReadOnlyModel):
    domain = models.CharField(max_length=254)
    table_name = models.CharField(max_length=254)
    lft = models.IntegerField()
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    level = models.IntegerField()
    country = models.ForeignKey('source_prp.CoreCountry', models.PROTECT, related_name='CoreCartodbtable_country')
    location_type = models.ForeignKey('source_prp.CoreGatewaytype', models.PROTECT, related_name='CoreCartodbtable_location_type')
    parent = models.ForeignKey('self', models.PROTECT, related_name='CoreCartodbtable_parent', blank=True, null=True)
    display_name = models.CharField(max_length=254)
    name_col = models.CharField(max_length=254)
    parent_code_col = models.CharField(max_length=254)
    pcode_col = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'core_cartodbtable'
        app_label = 'source_prp'


class CoreCountry(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=100)
    country_short_code = models.CharField(max_length=10, blank=True, null=True)
    long_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_country'
        app_label = 'source_prp'


class CoreGatewaytype(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=64)
    admin_level = models.SmallIntegerField()
    country = models.ForeignKey(CoreCountry, models.PROTECT, related_name='CoreGatewaytype_country')
    display_name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_gatewaytype'
        unique_together = (('country', 'admin_level'),)
        app_label = 'source_prp'


class CoreLocation(ReadOnlyModel):
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    p_code = models.CharField(max_length=32, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    point = models.GeometryField(blank=True, null=True)
    carto_db_table = models.ForeignKey(CoreCartodbtable, models.PROTECT, related_name='CoreLocation_carto_db_table', blank=True, null=True)
    gateway = models.ForeignKey(CoreGatewaytype, models.PROTECT, related_name='CoreLocation_gateway')
    parent = models.ForeignKey('self', models.PROTECT, related_name='CoreLocation_parent', blank=True, null=True)
    level = models.IntegerField()
    lft = models.IntegerField()
    rght = models.IntegerField()
    tree_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'core_location'
        unique_together = (('title', 'p_code'),)
        app_label = 'source_prp'


class CorePrprole(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=32)
    cluster = models.ForeignKey(ClusterCluster, models.PROTECT, related_name='CorePrprole_cluster', blank=True, null=True)
    user = models.ForeignKey(AccountUser, models.PROTECT, related_name='CorePrprole_user')
    workspace = models.ForeignKey('source_prp.CoreWorkspace', models.PROTECT, related_name='CorePrprole_workspace', blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'core_prprole'
        unique_together = (('user', 'role', 'workspace', 'cluster'),)
        app_label = 'source_prp'


class CoreResponseplan(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    plan_type = models.CharField(max_length=5)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    workspace = models.ForeignKey('source_prp.CoreWorkspace', models.PROTECT, related_name='CoreResponseplan_workspace')
    plan_custom_type_label = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_responseplan'
        unique_together = (('title', 'plan_type', 'workspace'),)
        app_label = 'source_prp'


class CoreWorkspace(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    workspace_code = models.CharField(unique=True, max_length=8)
    business_area_code = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    initial_zoom = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'core_workspace'
        app_label = 'source_prp'


class CoreWorkspaceCountries(ReadOnlyModel):
    workspace = models.ForeignKey(CoreWorkspace, models.PROTECT, related_name='CoreWorkspaceCountries_workspace')
    country = models.ForeignKey(CoreCountry, models.PROTECT, related_name='CoreWorkspaceCountries_country')

    class Meta:
        managed = False
        db_table = 'core_workspace_countries'
        unique_together = (('workspace', 'country'),)
        app_label = 'source_prp'


class DjangoCeleryBeatClockedschedule(ReadOnlyModel):
    clocked_time = models.DateTimeField()
    enabled = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_clockedschedule'
        app_label = 'source_prp'


class DjangoCeleryBeatCrontabschedule(ReadOnlyModel):
    minute = models.CharField(max_length=240)
    hour = models.CharField(max_length=96)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=124)
    month_of_year = models.CharField(max_length=64)
    timezone = models.CharField(max_length=63)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_crontabschedule'
        app_label = 'source_prp'


class DjangoCeleryBeatIntervalschedule(ReadOnlyModel):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_intervalschedule'
        app_label = 'source_prp'


class DjangoCeleryBeatPeriodictask(ReadOnlyModel):
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
    crontab = models.ForeignKey(DjangoCeleryBeatCrontabschedule, models.PROTECT, related_name='DjangoCeleryBeatPeriodictask_crontab', blank=True, null=True)
    interval = models.ForeignKey(DjangoCeleryBeatIntervalschedule, models.PROTECT, related_name='DjangoCeleryBeatPeriodictask_interval', blank=True, null=True)
    solar = models.ForeignKey('source_prp.DjangoCeleryBeatSolarschedule', models.PROTECT, related_name='DjangoCeleryBeatPeriodictask_solar', blank=True, null=True)
    one_off = models.BooleanField()
    start_time = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    headers = models.TextField()
    clocked = models.ForeignKey(DjangoCeleryBeatClockedschedule, models.PROTECT, related_name='DjangoCeleryBeatPeriodictask_clocked', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictask'
        app_label = 'source_prp'


class DjangoCeleryBeatPeriodictasks(ReadOnlyModel):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictasks'
        app_label = 'source_prp'


class DjangoCeleryBeatSolarschedule(ReadOnlyModel):
    event = models.CharField(max_length=24)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_solarschedule'
        unique_together = (('event', 'latitude', 'longitude'),)
        app_label = 'source_prp'


class DjangoCeleryResultsTaskresult(ReadOnlyModel):
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
        app_label = 'source_prp'


class DjangoContentType(ReadOnlyModel):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)
        app_label = 'source_prp'


class DjangoSite(ReadOnlyModel):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'
        app_label = 'source_prp'


class IndicatorDisaggregation(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField()
    response_plan = models.ForeignKey(CoreResponseplan, models.PROTECT, related_name='IndicatorDisaggregation_response_plan', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indicator_disaggregation'
        unique_together = (('name', 'response_plan'),)
        app_label = 'source_prp'


class IndicatorDisaggregationvalue(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=128)
    active = models.BooleanField()
    disaggregation = models.ForeignKey(IndicatorDisaggregation, models.PROTECT, related_name='IndicatorDisaggregationvalue_disaggregation')

    class Meta:
        managed = False
        db_table = 'indicator_disaggregationvalue'
        unique_together = (('disaggregation', 'value'),)
        app_label = 'source_prp'


class IndicatorIndicatorblueprint(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    title = models.TextField()
    unit = models.CharField(max_length=10)
    description = models.CharField(max_length=3072, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)
    subdomain = models.CharField(max_length=255, blank=True, null=True)
    disaggregatable = models.BooleanField()
    calculation_formula_across_periods = models.CharField(max_length=10)
    calculation_formula_across_locations = models.CharField(max_length=10)
    display_type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'indicator_indicatorblueprint'
        unique_together = (('external_id', 'external_source'),)
        app_label = 'source_prp'


class IndicatorIndicatorlocationdata(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    disaggregation = models.TextField()  # This field type is a guess.
    num_disaggregation = models.IntegerField()
    level_reported = models.IntegerField()
    disaggregation_reported_on = models.TextField()  # This field type is a guess.
    percentage_allocated = models.DecimalField(max_digits=5, decimal_places=2)
    is_locked = models.BooleanField()
    indicator_report = models.ForeignKey('source_prp.IndicatorIndicatorreport', models.PROTECT, related_name='IndicatorIndicatorlocationdata_indicator_report')
    location = models.ForeignKey(CoreLocation, models.PROTECT, related_name='IndicatorIndicatorlocationdata_location')

    class Meta:
        managed = False
        db_table = 'indicator_indicatorlocationdata'
        app_label = 'source_prp'


class IndicatorIndicatorreport(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    title = models.CharField(max_length=2048)
    time_period_start = models.DateField()
    time_period_end = models.DateField()
    due_date = models.DateField()
    submission_date = models.DateField(blank=True, null=True)
    frequency = models.CharField(max_length=3)
    total = models.TextField()  # This field type is a guess.
    remarks = models.TextField(blank=True, null=True)
    report_status = models.CharField(max_length=3)
    overall_status = models.CharField(max_length=3)
    narrative_assessment = models.TextField(blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    sent_back_feedback = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', models.PROTECT, related_name='IndicatorIndicatorreport_parent', blank=True, null=True)
    progress_report = models.ForeignKey('source_prp.UnicefProgressreport', models.PROTECT, related_name='IndicatorIndicatorreport_progress_report', blank=True, null=True)
    reportable = models.ForeignKey('source_prp.IndicatorReportable', models.PROTECT, related_name='IndicatorIndicatorreport_reportable')
    reporting_entity = models.ForeignKey('source_prp.IndicatorReportingentity', models.PROTECT, related_name='IndicatorIndicatorreport_reporting_entity')
    project = models.ForeignKey('source_prp.PartnerPartnerproject', models.PROTECT, related_name='IndicatorIndicatorreport_project', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indicator_indicatorreport'
        app_label = 'source_prp'


class IndicatorReportable(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    target = models.TextField()  # This field type is a guess.
    baseline = models.TextField()  # This field type is a guess.
    in_need = models.TextField(blank=True, null=True)  # This field type is a guess.
    assumptions = models.TextField(blank=True, null=True)
    means_of_verification = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    measurement_specifications = models.TextField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    numerator_label = models.CharField(max_length=256, blank=True, null=True)
    denominator_label = models.CharField(max_length=256, blank=True, null=True)
    start_date_of_reporting_period = models.DateField(blank=True, null=True)
    is_cluster_indicator = models.BooleanField()
    is_unicef_hf_indicator = models.BooleanField()
    contributes_to_partner = models.BooleanField()
    total = models.TextField()  # This field type is a guess.
    context_code = models.CharField(max_length=50, blank=True, null=True)
    object_id = models.IntegerField()
    frequency = models.CharField(max_length=3)
    cs_dates = models.TextField(blank=True, null=True)  # This field type is a guess.
    location_admin_refs = models.TextField(blank=True, null=True)  # This field type is a guess.
    active = models.BooleanField()
    blueprint = models.ForeignKey(IndicatorIndicatorblueprint, models.PROTECT, related_name='IndicatorReportable_blueprint', blank=True, null=True)
    ca_indicator_used_by_reporting_entity = models.ForeignKey('self', models.PROTECT, related_name='IndicatorReportable_ca_indicator_used_by_reporting_entity', blank=True, null=True)
    content_type = models.ForeignKey(DjangoContentType, models.PROTECT, related_name='IndicatorReportable_content_type')
    parent_indicator = models.ForeignKey('self', models.PROTECT, related_name='IndicatorReportable_parent_indicator', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indicator_reportable'
        app_label = 'source_prp'


class IndicatorReportableDisaggregations(ReadOnlyModel):
    reportable = models.ForeignKey(IndicatorReportable, models.PROTECT, related_name='IndicatorReportableDisaggregations_reportable')
    disaggregation = models.ForeignKey(IndicatorDisaggregation, models.PROTECT, related_name='IndicatorReportableDisaggregations_disaggregation')

    class Meta:
        managed = False
        db_table = 'indicator_reportable_disaggregations'
        unique_together = (('reportable', 'disaggregation'),)
        app_label = 'source_prp'


class IndicatorReportable locationgoal(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    target = models.TextField()  # This field type is a guess.
    baseline = models.TextField()  # This field type is a guess.
    in_need = models.TextField(blank=True, null=True)  # This field type is a guess.
    location = models.ForeignKey(CoreLocation, models.PROTECT, related_name='IndicatorReportablelocationgoal_location')
    reportable = models.ForeignKey(IndicatorReportable, models.PROTECT, related_name='IndicatorReportablelocationgoal_reportable')
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'indicator_reportablelocationgoal'
        unique_together = (('reportable', 'location'),)
        app_label = 'source_prp'


class IndicatorReportingentity(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    title = models.CharField(unique=True, max_length=256)

    class Meta:
        managed = False
        db_table = 'indicator_reportingentity'
        app_label = 'source_prp'


class PartnerPartner(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    short_title = models.CharField(max_length=50)
    alternate_title = models.CharField(max_length=255, blank=True, null=True)
    partner_type = models.CharField(max_length=3)
    shared_partner = models.CharField(max_length=3)
    cso_type = models.CharField(max_length=3, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    last_assessment_date = models.DateField(blank=True, null=True)
    core_values_assessment_date = models.DateField(blank=True, null=True)
    street_address = models.CharField(max_length=512, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    postal_code = models.CharField(max_length=32, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    total_ct_cp = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_ct_cy = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vendor_number = models.CharField(unique=True, max_length=30, blank=True, null=True)
    alternate_id = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=50, blank=True, null=True)
    basis_for_risk_rating = models.CharField(max_length=50, blank=True, null=True)
    ocha_external_id = models.CharField(unique=True, max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partner'
        unique_together = (('title', 'vendor_number'),)
        app_label = 'source_prp'


class PartnerPartnerClusters(ReadOnlyModel):
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerClusters_partner')
    cluster = models.ForeignKey(ClusterCluster, models.PROTECT, related_name='PartnerPartnerClusters_cluster')

    class Meta:
        managed = False
        db_table = 'partner_partner_clusters'
        unique_together = (('partner', 'cluster'),)
        app_label = 'source_prp'


class PartnerPartneractivity(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    title = models.CharField(max_length=2048)
    cluster_activity = models.ForeignKey(ClusterClusteractivity, models.PROTECT, related_name='PartnerPartneractivity_cluster_activity', blank=True, null=True)
    cluster_objective = models.ForeignKey(ClusterClusterobjective, models.PROTECT, related_name='PartnerPartneractivity_cluster_objective', blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartneractivity_partner')

    class Meta:
        managed = False
        db_table = 'partner_partneractivity'
        app_label = 'source_prp'


class PartnerPartneractivityLocations(ReadOnlyModel):
    partneractivity = models.ForeignKey(PartnerPartneractivity, models.PROTECT, related_name='PartnerPartneractivityLocations_partneractivity')
    location = models.ForeignKey(CoreLocation, models.PROTECT, related_name='PartnerPartneractivityLocations_location')

    class Meta:
        managed = False
        db_table = 'partner_partneractivity_locations'
        unique_together = (('partneractivity', 'location'),)
        app_label = 'source_prp'


class PartnerPartneractivityprojectcontext(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=3)
    activity = models.ForeignKey(PartnerPartneractivity, models.PROTECT, related_name='PartnerPartneractivityprojectcontext_activity')
    project = models.ForeignKey('source_prp.PartnerPartnerproject', models.PROTECT, related_name='PartnerPartneractivityprojectcontext_project')

    class Meta:
        managed = False
        db_table = 'partner_partneractivityprojectcontext'
        unique_together = (('project', 'activity'),)
        app_label = 'source_prp'


class PartnerPartnerproject(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    code = models.TextField(unique=True, blank=True, null=True)
    type = models.CharField(max_length=3, blank=True, null=True)
    title = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    additional_information = models.CharField(max_length=255, blank=True, null=True)
    custom_fields = models.TextField()  # This field type is a guess.
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=3)
    agency_name = models.TextField(blank=True, null=True)
    agency_type = models.TextField(blank=True, null=True)
    prioritization = models.TextField(blank=True, null=True)
    total_budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    funding_source = models.TextField(blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerproject_partner')

    class Meta:
        managed = False
        db_table = 'partner_partnerproject'
        app_label = 'source_prp'


class PartnerPartnerprojectAdditionalPartners(ReadOnlyModel):
    partnerproject = models.ForeignKey(PartnerPartnerproject, models.PROTECT, related_name='PartnerPartnerprojectAdditionalPartners_partnerproject')
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerprojectAdditionalPartners_partner')

    class Meta:
        managed = False
        db_table = 'partner_partnerproject_additional_partners'
        unique_together = (('partnerproject', 'partner'),)
        app_label = 'source_prp'


class PartnerPartnerprojectClusters(ReadOnlyModel):
    partnerproject = models.ForeignKey(PartnerPartnerproject, models.PROTECT, related_name='PartnerPartnerprojectClusters_partnerproject')
    cluster = models.ForeignKey(ClusterCluster, models.PROTECT, related_name='PartnerPartnerprojectClusters_cluster')

    class Meta:
        managed = False
        db_table = 'partner_partnerproject_clusters'
        unique_together = (('partnerproject', 'cluster'),)
        app_label = 'source_prp'


class PartnerPartnerprojectLocations(ReadOnlyModel):
    partnerproject = models.ForeignKey(PartnerPartnerproject, models.PROTECT, related_name='PartnerPartnerprojectLocations_partnerproject')
    location = models.ForeignKey(CoreLocation, models.PROTECT, related_name='PartnerPartnerprojectLocations_location')

    class Meta:
        managed = False
        db_table = 'partner_partnerproject_locations'
        unique_together = (('partnerproject', 'location'),)
        app_label = 'source_prp'


class PartnerPartnerprojectfunding(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    required_funding = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    internal_funding = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    cerf_funding = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    cbpf_funding = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    bilateral_funding = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    unicef_funding = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    wfp_funding = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    project = models.OneToOneField(PartnerPartnerproject, models.PROTECT, related_name='PartnerPartnerprojectfunding_project')

    class Meta:
        managed = False
        db_table = 'partner_partnerprojectfunding'
        app_label = 'source_prp'


class UnicefLowerleveloutput(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    title = models.CharField(max_length=512)
    active = models.BooleanField()
    cp_output = models.ForeignKey('source_prp.UnicefPdresultlink', models.PROTECT, related_name='UnicefLowerleveloutput_cp_output')
    external_business_area_code = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_lowerleveloutput'
        unique_together = (('external_id', 'external_business_area_code', 'cp_output'),)
        app_label = 'source_prp'


class UnicefPdresultlink(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    title = models.CharField(max_length=512)
    external_cp_output_id = models.IntegerField()
    programme_document = models.ForeignKey('source_prp.UnicefProgrammedocument', models.PROTECT, related_name='UnicefPdresultlink_programme_document')
    external_business_area_code = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_pdresultlink'
        unique_together = (('external_id', 'external_business_area_code', 'external_cp_output_id'),)
        app_label = 'source_prp'


class UnicefPerson(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'unicef_person'
        app_label = 'source_prp'


class UnicefProgrammedocument(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    agreement = models.CharField(max_length=255)
    document_type = models.CharField(max_length=4)
    reference_number = models.CharField(max_length=255)
    title = models.CharField(max_length=512)
    unicef_office = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=256)
    contributing_to_cluster = models.BooleanField()
    frequency = models.CharField(max_length=3)
    budget = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    budget_currency = models.CharField(max_length=16)
    cso_contribution = models.DecimalField(max_digits=64, decimal_places=2)
    cso_contribution_currency = models.CharField(max_length=16)
    total_unicef_cash = models.DecimalField(max_digits=64, decimal_places=2)
    total_unicef_cash_currency = models.CharField(max_length=16)
    in_kind_amount = models.DecimalField(max_digits=64, decimal_places=2)
    in_kind_amount_currency = models.CharField(max_length=16)
    funds_received_to_date = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    funds_received_to_date_currency = models.CharField(max_length=16, blank=True, null=True)
    amendments = models.TextField()  # This field type is a guess.
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='UnicefProgrammedocument_partner')
    workspace = models.ForeignKey(CoreWorkspace, models.PROTECT, related_name='UnicefProgrammedocument_workspace')
    external_business_area_code = models.CharField(max_length=32, blank=True, null=True)
    funds_received_to_date_percent = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_programmedocument'
        unique_together = (('external_id', 'external_business_area_code', 'workspace'),)
        app_label = 'source_prp'


class UnicefProgrammedocumentPartnerFocalPoint(ReadOnlyModel):
    programmedocument = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='UnicefProgrammedocumentPartnerFocalPoint_programmedocument')
    person = models.ForeignKey(UnicefPerson, models.PROTECT, related_name='UnicefProgrammedocumentPartnerFocalPoint_person')

    class Meta:
        managed = False
        db_table = 'unicef_programmedocument_partner_focal_point'
        unique_together = (('programmedocument', 'person'),)
        app_label = 'source_prp'


class UnicefProgrammedocumentSections(ReadOnlyModel):
    programmedocument = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='UnicefProgrammedocumentSections_programmedocument')
    section = models.ForeignKey('source_prp.UnicefSection', models.PROTECT, related_name='UnicefProgrammedocumentSections_section')

    class Meta:
        managed = False
        db_table = 'unicef_programmedocument_sections'
        unique_together = (('programmedocument', 'section'),)
        app_label = 'source_prp'


class UnicefProgrammedocumentUnicefFocalPoint(ReadOnlyModel):
    programmedocument = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='UnicefProgrammedocumentUnicefFocalPoint_programmedocument')
    person = models.ForeignKey(UnicefPerson, models.PROTECT, related_name='UnicefProgrammedocumentUnicefFocalPoint_person')

    class Meta:
        managed = False
        db_table = 'unicef_programmedocument_unicef_focal_point'
        unique_together = (('programmedocument', 'person'),)
        app_label = 'source_prp'


class UnicefProgrammedocumentUnicefOfficers(ReadOnlyModel):
    programmedocument = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='UnicefProgrammedocumentUnicefOfficers_programmedocument')
    person = models.ForeignKey(UnicefPerson, models.PROTECT, related_name='UnicefProgrammedocumentUnicefOfficers_person')

    class Meta:
        managed = False
        db_table = 'unicef_programmedocument_unicef_officers'
        unique_together = (('programmedocument', 'person'),)
        app_label = 'source_prp'


class UnicefProgressreport(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    partner_contribution_to_date = models.TextField(blank=True, null=True)
    challenges_in_the_reporting_period = models.TextField(blank=True, null=True)
    proposed_way_forward = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=3)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    due_date = models.DateField()
    submission_date = models.DateField(blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    review_overall_status = models.CharField(max_length=3, blank=True, null=True)
    sent_back_feedback = models.TextField(blank=True, null=True)
    report_number = models.IntegerField()
    report_type = models.CharField(max_length=3)
    is_final = models.BooleanField()
    narrative = models.TextField(blank=True, null=True)
    programme_document = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='UnicefProgressreport_programme_document')
    submitted_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='UnicefProgressreport_submitted_by', blank=True, null=True)
    submitting_user = models.ForeignKey(AccountUser, models.PROTECT, related_name='UnicefProgressreport_submitting_user', blank=True, null=True)
    reviewed_by_email = models.CharField(max_length=256, blank=True, null=True)
    reviewed_by_external_id = models.IntegerField(blank=True, null=True)
    reviewed_by_name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_progressreport'
        unique_together = (('programme_document', 'report_type', 'report_number'),)
        app_label = 'source_prp'


class UnicefProgressreportattachment(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    file = models.CharField(max_length=500)
    type = models.CharField(max_length=5)
    progress_report = models.ForeignKey(UnicefProgressreport, models.PROTECT, related_name='UnicefProgressreportattachment_progress_report')

    class Meta:
        managed = False
        db_table = 'unicef_progressreportattachment'
        app_label = 'source_prp'


class UnicefReportingperioddates(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    report_type = models.CharField(max_length=3)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    programme_document = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='UnicefReportingperioddates_programme_document')
    external_business_area_code = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_reportingperioddates'
        unique_together = (('external_id', 'external_business_area_code', 'report_type', 'programme_document'),)
        app_label = 'source_prp'


class UnicefSection(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'unicef_section'
        app_label = 'source_prp'
