# flake8: noqa F405.
# This is an auto-generated PRP model module.
# Generated on 2019-08-20 13:50:08.824966
from django.contrib.gis.db import models

from etools_datamart.apps.core.readonly import ReadOnlyModel


class AccountUser(ReadOnlyModel):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    organization = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    partner = models.ForeignKey('prp.PartnerPartner', models.PROTECT, related_name='+', blank=True, null=True)
    position = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_user'
        app_label = 'prp'


class AccountUserGroups(ReadOnlyModel):
    user_id = models.IntegerField()
    group = models.ForeignKey('prp.AuthGroup', models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'account_user_groups'
        unique_together = (('user_id', 'group'),)
        app_label = 'prp'


class AccountUserUserPermissions(ReadOnlyModel):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'account_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)
        app_label = 'prp'


class AccountUserprofile(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'account_userprofile'
        app_label = 'prp'


class AuthGroup(ReadOnlyModel):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'
        app_label = 'prp'


class AuthGroupPermissions(ReadOnlyModel):
    group = models.ForeignKey(AuthGroup, models.PROTECT, related_name='+')
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission_id'),)
        app_label = 'prp'


class AuthPermission(ReadOnlyModel):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('prp.DjangoContentType', models.PROTECT, related_name='+')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        app_label = 'prp'


class AuthtokenToken(ReadOnlyModel):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'
        app_label = 'prp'


class ClusterCluster(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=32)
    imported_type = models.TextField(blank=True, null=True)
    response_plan = models.ForeignKey('prp.CoreResponseplan', models.PROTECT, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cluster_cluster'
        app_label = 'prp'


class ClusterClusteractivity(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    title = models.TextField()
    cluster_objective_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cluster_clusteractivity'
        unique_together = (('external_id', 'external_source'),)
        app_label = 'prp'


class ClusterClusteractivityLocations(ReadOnlyModel):
    clusteractivity_id = models.IntegerField()
    location = models.ForeignKey('prp.CoreLocation', models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'cluster_clusteractivity_locations'
        unique_together = (('clusteractivity_id', 'location'),)
        app_label = 'prp'


class ClusterClusterobjective(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    title = models.TextField()
    cluster_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cluster_clusterobjective'
        unique_together = (('external_id', 'external_source'),)
        app_label = 'prp'


class ClusterClusterobjectiveLocations(ReadOnlyModel):
    clusterobjective_id = models.IntegerField()
    location = models.ForeignKey('prp.CoreLocation', models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'cluster_clusterobjective_locations'
        unique_together = (('clusterobjective_id', 'location'),)
        app_label = 'prp'


class CoreCartodbtable(ReadOnlyModel):
    domain = models.CharField(max_length=254)
    table_name = models.CharField(max_length=254)
    lft = models.IntegerField()
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    level = models.IntegerField()
    country_id = models.IntegerField()
    location_type_id = models.IntegerField()
    parent_id = models.IntegerField(blank=True, null=True)
    display_name = models.CharField(max_length=254)
    name_col = models.CharField(max_length=254)
    parent_code_col = models.CharField(max_length=254)
    pcode_col = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'core_cartodbtable'
        app_label = 'prp'


class CoreCountry(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=100)
    country_short_code = models.CharField(max_length=10, blank=True, null=True)
    long_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_country'
        app_label = 'prp'


class CoreGatewaytype(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=64)
    admin_level = models.SmallIntegerField()
    country_id = models.IntegerField()
    display_name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_gatewaytype'
        app_label = 'prp'


class CoreLocation(ReadOnlyModel):
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    p_code = models.CharField(max_length=32, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    point = models.GeometryField(blank=True, null=True)
    carto_db_table_id = models.IntegerField(blank=True, null=True)
    gateway_id = models.IntegerField()
    parent = models.ForeignKey('self', models.PROTECT, related_name='+', blank=True, null=True)
    level = models.IntegerField()
    lft = models.IntegerField()
    rght = models.IntegerField()
    tree_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'core_location'
        unique_together = (('title', 'p_code'),)
        app_label = 'prp'


class CorePrprole(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=32)
    cluster_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()
    workspace = models.ForeignKey('prp.CoreWorkspace', models.PROTECT, related_name='+', blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'core_prprole'
        unique_together = (('external_id', 'external_source'),)
        app_label = 'prp'


class CoreResponseplan(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    plan_type = models.CharField(max_length=5)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    workspace = models.ForeignKey('prp.CoreWorkspace', models.PROTECT, related_name='+')
    plan_custom_type_label = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_responseplan'
        unique_together = (('title', 'plan_type', 'workspace'),)
        app_label = 'prp'


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
        app_label = 'prp'


class CoreWorkspaceCountries(ReadOnlyModel):
    workspace = models.ForeignKey(CoreWorkspace, models.PROTECT, related_name='+')
    country_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'core_workspace_countries'
        unique_together = (('workspace', 'country_id'),)
        app_label = 'prp'


class DjangoContentType(ReadOnlyModel):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)
        app_label = 'prp'


class DjangoSite(ReadOnlyModel):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'
        app_label = 'prp'


class IndicatorDisaggregation(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField()
    response_plan = models.ForeignKey(CoreResponseplan, models.PROTECT, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indicator_disaggregation'
        unique_together = (('name', 'response_plan'),)
        app_label = 'prp'


class IndicatorDisaggregationvalue(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    external_source = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=128)
    active = models.BooleanField()
    disaggregation = models.ForeignKey(IndicatorDisaggregation, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'indicator_disaggregationvalue'
        unique_together = (('disaggregation', 'value'),)
        app_label = 'prp'


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
        app_label = 'prp'


class IndicatorIndicatorlocationdata(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    disaggregation = models.TextField()  # This field type is a guess.
    num_disaggregation = models.IntegerField()
    level_reported = models.IntegerField()
    disaggregation_reported_on = models.TextField()  # This field type is a guess.
    percentage_allocated = models.DecimalField(max_digits=5, decimal_places=2)
    is_locked = models.BooleanField()
    indicator_report = models.ForeignKey('prp.IndicatorIndicatorreport', models.PROTECT, related_name='+')
    location = models.ForeignKey(CoreLocation, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'indicator_indicatorlocationdata'
        app_label = 'prp'


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
    parent = models.ForeignKey('self', models.PROTECT, related_name='+', blank=True, null=True)
    progress_report = models.ForeignKey('prp.UnicefProgressreport', models.PROTECT, related_name='+', blank=True, null=True)
    reportable = models.ForeignKey('prp.IndicatorReportable', models.PROTECT, related_name='+')
    reporting_entity = models.ForeignKey('prp.IndicatorReportingentity', models.PROTECT, related_name='+')
    project = models.ForeignKey('prp.PartnerPartnerproject', models.PROTECT, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indicator_indicatorreport'
        app_label = 'prp'


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
    blueprint = models.ForeignKey(IndicatorIndicatorblueprint, models.PROTECT, related_name='+', blank=True, null=True)
    ca_indicator_used_by_reporting_entity = models.ForeignKey('self', models.PROTECT, related_name='+', blank=True, null=True)
    content_type = models.ForeignKey(DjangoContentType, models.PROTECT, related_name='+')
    parent_indicator = models.ForeignKey('self', models.PROTECT, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indicator_reportable'
        app_label = 'prp'


class IndicatorReportableDisaggregations(ReadOnlyModel):
    reportable = models.ForeignKey(IndicatorReportable, models.PROTECT, related_name='+')
    disaggregation = models.ForeignKey(IndicatorDisaggregation, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'indicator_reportable_disaggregations'
        unique_together = (('reportable', 'disaggregation'),)
        app_label = 'prp'


class IndicatorReportablelocationgoal(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    target = models.TextField()  # This field type is a guess.
    baseline = models.TextField()  # This field type is a guess.
    in_need = models.TextField(blank=True, null=True)  # This field type is a guess.
    location = models.ForeignKey(CoreLocation, models.PROTECT, related_name='+')
    reportable = models.ForeignKey(IndicatorReportable, models.PROTECT, related_name='+')
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'indicator_reportablelocationgoal'
        unique_together = (('reportable', 'location'),)
        app_label = 'prp'


class IndicatorReportingentity(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    title = models.CharField(unique=True, max_length=256)

    class Meta:
        managed = False
        db_table = 'indicator_reportingentity'
        app_label = 'prp'


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
        app_label = 'prp'


class PartnerPartnerClusters(ReadOnlyModel):
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='+')
    cluster_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'partner_partner_clusters'
        unique_together = (('partner', 'cluster_id'),)
        app_label = 'prp'


class PartnerPartneractivity(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    title = models.CharField(max_length=2048)
    cluster_activity_id = models.IntegerField(blank=True, null=True)
    cluster_objective_id = models.IntegerField(blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'partner_partneractivity'
        app_label = 'prp'


class PartnerPartneractivityLocations(ReadOnlyModel):
    partneractivity = models.ForeignKey(PartnerPartneractivity, models.PROTECT, related_name='+')
    location = models.ForeignKey(CoreLocation, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'partner_partneractivity_locations'
        unique_together = (('partneractivity', 'location'),)
        app_label = 'prp'


class PartnerPartneractivityprojectcontext(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=3)
    activity = models.ForeignKey(PartnerPartneractivity, models.PROTECT, related_name='+')
    project = models.ForeignKey('prp.PartnerPartnerproject', models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'partner_partneractivityprojectcontext'
        unique_together = (('project', 'activity'),)
        app_label = 'prp'


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
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'partner_partnerproject'
        app_label = 'prp'


class PartnerPartnerprojectAdditionalPartners(ReadOnlyModel):
    partnerproject = models.ForeignKey(PartnerPartnerproject, models.PROTECT, related_name='+')
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'partner_partnerproject_additional_partners'
        unique_together = (('partnerproject', 'partner'),)
        app_label = 'prp'


class PartnerPartnerprojectClusters(ReadOnlyModel):
    partnerproject = models.ForeignKey(PartnerPartnerproject, models.PROTECT, related_name='+')
    cluster_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'partner_partnerproject_clusters'
        unique_together = (('partnerproject', 'cluster_id'),)
        app_label = 'prp'


class PartnerPartnerprojectLocations(ReadOnlyModel):
    partnerproject = models.ForeignKey(PartnerPartnerproject, models.PROTECT, related_name='+')
    location = models.ForeignKey(CoreLocation, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'partner_partnerproject_locations'
        unique_together = (('partnerproject', 'location'),)
        app_label = 'prp'


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
    project = models.OneToOneField(PartnerPartnerproject, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'partner_partnerprojectfunding'
        app_label = 'prp'


class UnicefLowerleveloutput(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    title = models.CharField(max_length=512)
    active = models.BooleanField()
    cp_output = models.ForeignKey('prp.UnicefPdresultlink', models.PROTECT, related_name='+')
    external_business_area_code = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_lowerleveloutput'
        unique_together = (('external_id', 'external_business_area_code'),)
        app_label = 'prp'


class UnicefPdresultlink(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    title = models.CharField(max_length=512)
    external_cp_output_id = models.IntegerField()
    programme_document = models.ForeignKey('prp.UnicefProgrammedocument', models.PROTECT, related_name='+')
    external_business_area_code = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_pdresultlink'
        unique_together = (('external_id', 'external_business_area_code', 'external_cp_output_id'),)
        app_label = 'prp'


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
        app_label = 'prp'


class UnicefProgrammedocument(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    agreement = models.CharField(max_length=255)
    document_type = models.CharField(max_length=3)
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
    funds_received_to_date = models.DecimalField(max_digits=64, decimal_places=2)
    funds_received_to_date_currency = models.CharField(max_length=16, blank=True, null=True)
    amendments = models.TextField()  # This field type is a guess.
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='+')
    workspace = models.ForeignKey(CoreWorkspace, models.PROTECT, related_name='+')
    external_business_area_code = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_programmedocument'
        unique_together = (('external_id', 'external_business_area_code', 'workspace'),)
        app_label = 'prp'


class UnicefProgrammedocumentPartnerFocalPoint(ReadOnlyModel):
    programmedocument = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='+')
    person = models.ForeignKey(UnicefPerson, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'unicef_programmedocument_partner_focal_point'
        unique_together = (('programmedocument', 'person'),)
        app_label = 'prp'


class UnicefProgrammedocumentSections(ReadOnlyModel):
    programmedocument = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='+')
    section = models.ForeignKey('prp.UnicefSection', models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'unicef_programmedocument_sections'
        unique_together = (('programmedocument', 'section'),)
        app_label = 'prp'


class UnicefProgrammedocumentUnicefFocalPoint(ReadOnlyModel):
    programmedocument = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='+')
    person = models.ForeignKey(UnicefPerson, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'unicef_programmedocument_unicef_focal_point'
        unique_together = (('programmedocument', 'person'),)
        app_label = 'prp'


class UnicefProgrammedocumentUnicefOfficers(ReadOnlyModel):
    programmedocument = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='+')
    person = models.ForeignKey(UnicefPerson, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'unicef_programmedocument_unicef_officers'
        unique_together = (('programmedocument', 'person'),)
        app_label = 'prp'


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
    programme_document = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='+')
    submitted_by_id = models.IntegerField(blank=True, null=True)
    submitting_user_id = models.IntegerField(blank=True, null=True)
    reviewed_by_email = models.CharField(max_length=256, blank=True, null=True)
    reviewed_by_external_id = models.IntegerField(blank=True, null=True)
    reviewed_by_name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_progressreport'
        unique_together = (('programme_document', 'report_type', 'report_number'),)
        app_label = 'prp'


class UnicefProgressreportattachment(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    file = models.CharField(max_length=500)
    type = models.CharField(max_length=5)
    progress_report = models.ForeignKey(UnicefProgressreport, models.PROTECT, related_name='+')

    class Meta:
        managed = False
        db_table = 'unicef_progressreportattachment'
        app_label = 'prp'


class UnicefReportingperioddates(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    report_type = models.CharField(max_length=3)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    programme_document = models.ForeignKey(UnicefProgrammedocument, models.PROTECT, related_name='+')
    external_business_area_code = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_reportingperioddates'
        unique_together = (('external_id', 'external_business_area_code', 'report_type', 'programme_document'),)
        app_label = 'prp'


class UnicefSection(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    external_id = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'unicef_section'
        app_label = 'prp'
