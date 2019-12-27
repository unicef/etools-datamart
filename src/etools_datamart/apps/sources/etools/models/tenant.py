# flake8: noqa F405.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from etools_datamart.apps.multitenant import models


class ActionPointsActionpoint(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=10)
    description = models.TextField()
    due_date = models.DateField(blank=True, null=True)
    date_of_completion = models.DateTimeField(blank=True, null=True)
    assigned_by = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='ActionPointsActionpoint_assigned_by')
    assigned_to = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='ActionPointsActionpoint_assigned_to')
    author = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='ActionPointsActionpoint_author')
    cp_output = models.ForeignKey('ReportsResult', models.DO_NOTHING, related_name='ActionPointsActionpoint_cp_output', blank=True, null=True)
    engagement = models.ForeignKey('AuditEngagement', models.DO_NOTHING, related_name='ActionPointsActionpoint_engagement', blank=True, null=True)
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, related_name='ActionPointsActionpoint_intervention', blank=True, null=True)
    location = models.ForeignKey('LocationsLocation', models.DO_NOTHING, related_name='ActionPointsActionpoint_location', blank=True, null=True)
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='ActionPointsActionpoint_office', blank=True, null=True)
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='ActionPointsActionpoint_partner', blank=True, null=True)
    section = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='ActionPointsActionpoint_section', blank=True, null=True)
    tpm_activity = models.ForeignKey('TpmTpmactivity', models.DO_NOTHING, related_name='ActionPointsActionpoint_tpm_activity', blank=True, null=True)
    high_priority = models.BooleanField()
    travel_activity = models.ForeignKey('T2FTravelactivity', models.DO_NOTHING, related_name='ActionPointsActionpoint_travel_activity', blank=True, null=True)
    category = models.ForeignKey('CategoriesCategory', models.DO_NOTHING, related_name='ActionPointsActionpoint_category', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action_points_actionpoint'


class ActivitiesActivity(models.TenantModel):
    date = models.DateField(blank=True, null=True)
    cp_output = models.ForeignKey('ReportsResult', models.DO_NOTHING, related_name='ActivitiesActivity_cp_output', blank=True, null=True)
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, related_name='ActivitiesActivity_intervention', blank=True, null=True)
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='ActivitiesActivity_partner', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activities_activity'


class ActivitiesActivityLocations(models.TenantModel):
    activity = models.ForeignKey(ActivitiesActivity, models.DO_NOTHING, related_name='ActivitiesActivityLocations_activity')
    location = models.ForeignKey('LocationsLocation', models.DO_NOTHING, related_name='ActivitiesActivityLocations_location')

    class Meta:
        managed = False
        db_table = 'activities_activity_locations'
        unique_together = (('activity', 'location'),)


class ActstreamAction(models.TenantModel):
    actor_object_id = models.CharField(max_length=255)
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    public = models.BooleanField()
    data = models.TextField(blank=True, null=True)
    action_object_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='ActstreamAction_action_object_content_type', blank=True, null=True)
    actor_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='ActstreamAction_actor_content_type')
    target_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='ActstreamAction_target_content_type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actstream_action'


class ActstreamFollow(models.TenantModel):
    object_id = models.CharField(max_length=255)
    actor_only = models.BooleanField()
    started = models.DateTimeField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='ActstreamFollow_content_type')
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='ActstreamFollow_user')

    class Meta:
        managed = False
        db_table = 'actstream_follow'
        unique_together = (('content_type', 'object_id', 'user'),)


# class AttachmentsAttachment(models.TenantModel):
#     created = models.DateTimeField()
#     modified = models.DateTimeField()
#     file = models.CharField(max_length=1024, blank=True, null=True)
#     hyperlink = models.CharField(max_length=255)
#     object_id = models.IntegerField(blank=True, null=True)
#     code = models.CharField(max_length=64)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='AttachmentsAttachment_content_type', blank=True, null=True)
#     file_type = models.ForeignKey('AttachmentsFiletype', models.DO_NOTHING, related_name='AttachmentsAttachment_file_type', blank=True, null=True)
#     uploaded_by = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='AttachmentsAttachment_uploaded_by', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'attachments_attachment'


class AttachmentsAttachmentflat(models.TenantModel):
    partner = models.CharField(max_length=255)
    partner_type = models.CharField(max_length=150)
    vendor_number = models.CharField(max_length=50)
    pd_ssfa_number = models.CharField(max_length=64)
    file_type = models.CharField(max_length=100)
    file_link = models.CharField(max_length=1024)
    uploaded_by = models.CharField(max_length=255)
    created = models.CharField(max_length=50)
    attachment = models.ForeignKey('UnicefAttachmentsAttachment', models.DO_NOTHING, related_name='AttachmentsAttachmentflat_attachment')
    filename = models.CharField(max_length=1024)
    agreement_reference_number = models.CharField(max_length=100)
    object_link = models.CharField(max_length=200)
    source = models.CharField(max_length=150)
    pd_ssfa = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attachments_attachmentflat'


class AttachmentsFiletype(models.TenantModel):
    order = models.IntegerField()
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    label = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'attachments_filetype'
        unique_together = (('code', 'name'),)


class AuditAudit(models.TenantModel):
    engagement_ptr = models.OneToOneField('AuditEngagement', models.DO_NOTHING, related_name='AuditAudit_engagement_ptr')
    audited_expenditure = models.DecimalField(max_digits=20, decimal_places=2)
    financial_findings = models.DecimalField(max_digits=20, decimal_places=2)
    audit_opinion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'audit_audit'


class AuditDetailedfindinginfo(models.TenantModel):
    finding = models.TextField()
    recommendation = models.TextField()
    micro_assesment = models.ForeignKey('AuditMicroassessment', models.DO_NOTHING, related_name='AuditDetailedfindinginfo_micro_assesment')

    class Meta:
        managed = False
        db_table = 'audit_detailedfindinginfo'


class AuditEngagement(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=30)
    partner_contacted_at = models.DateField(blank=True, null=True)
    engagement_type = models.CharField(max_length=10)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    total_value = models.DecimalField(max_digits=20, decimal_places=2)
    date_of_field_visit = models.DateField(blank=True, null=True)
    date_of_draft_report_to_ip = models.DateField(blank=True, null=True)
    date_of_comments_by_ip = models.DateField(blank=True, null=True)
    date_of_draft_report_to_unicef = models.DateField(blank=True, null=True)
    date_of_comments_by_unicef = models.DateField(blank=True, null=True)
    date_of_report_submit = models.DateField(blank=True, null=True)
    date_of_final_report = models.DateField(blank=True, null=True)
    date_of_cancel = models.DateField(blank=True, null=True)
    amount_refunded = models.DecimalField(max_digits=20, decimal_places=2)
    additional_supporting_documentation_provided = models.DecimalField(max_digits=20, decimal_places=2)
    justification_provided_and_accepted = models.DecimalField(max_digits=20, decimal_places=2)
    write_off_required = models.DecimalField(max_digits=20, decimal_places=2)
    cancel_comment = models.TextField()
    explanation_for_additional_information = models.TextField()
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='AuditEngagement_partner')
    joint_audit = models.BooleanField()
    agreement = models.ForeignKey('PurchaseOrderPurchaseorder', models.DO_NOTHING, related_name='AuditEngagement_agreement')
    po_item = models.ForeignKey('PurchaseOrderPurchaseorderitem', models.DO_NOTHING, related_name='AuditEngagement_po_item', blank=True, null=True)
    shared_ip_with = models.TextField()  # This field type is a guess.
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'audit_engagement'


class AuditEngagementActivePd(models.TenantModel):
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING, related_name='AuditEngagementActivePd_engagement')
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, related_name='AuditEngagementActivePd_intervention')

    class Meta:
        managed = False
        db_table = 'audit_engagement_active_pd'
        unique_together = (('engagement', 'intervention'),)


class AuditEngagementAuthorizedOfficers(models.TenantModel):
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING, related_name='AuditEngagementAuthorizedOfficers_engagement')
    partnerstaffmember = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, related_name='AuditEngagementAuthorizedOfficers_partnerstaffmember')

    class Meta:
        managed = False
        db_table = 'audit_engagement_authorized_officers'
        unique_together = (('engagement', 'partnerstaffmember'),)


class AuditEngagementStaffMembers(models.TenantModel):
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING, related_name='AuditEngagementStaffMembers_engagement')
    auditorstaffmember = models.ForeignKey('PurchaseOrderAuditorstaffmember', models.DO_NOTHING, related_name='AuditEngagementStaffMembers_auditorstaffmember')

    class Meta:
        managed = False
        db_table = 'audit_engagement_staff_members'
        unique_together = (('auditorstaffmember', 'engagement'),)


class AuditFinancialfinding(models.TenantModel):
    title = models.CharField(max_length=255)
    local_amount = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    recommendation = models.TextField()
    ip_comments = models.TextField()
    audit = models.ForeignKey(AuditAudit, models.DO_NOTHING, related_name='AuditFinancialfinding_audit')

    class Meta:
        managed = False
        db_table = 'audit_financialfinding'


class AuditFinding(models.TenantModel):
    priority = models.CharField(max_length=4)
    category_of_observation = models.CharField(max_length=100)
    recommendation = models.TextField()
    agreed_action_by_ip = models.TextField()
    deadline_of_action = models.DateField(blank=True, null=True)
    spot_check = models.ForeignKey('AuditSpotcheck', models.DO_NOTHING, related_name='AuditFinding_spot_check')

    class Meta:
        managed = False
        db_table = 'audit_finding'


class AuditKeyinternalcontrol(models.TenantModel):
    recommendation = models.TextField()
    audit_observation = models.TextField()
    ip_response = models.TextField()
    audit = models.ForeignKey(AuditAudit, models.DO_NOTHING, related_name='AuditKeyinternalcontrol_audit')

    class Meta:
        managed = False
        db_table = 'audit_keyinternalcontrol'


class AuditMicroassessment(models.TenantModel):
    engagement_ptr = models.OneToOneField(AuditEngagement, models.DO_NOTHING, related_name='AuditMicroassessment_engagement_ptr')

    class Meta:
        managed = False
        db_table = 'audit_microassessment'


class AuditRisk(models.TenantModel):
    value = models.SmallIntegerField(blank=True, null=True)
    extra = models.TextField(blank=True, null=True)  # This field type is a guess.
    blueprint = models.ForeignKey('AuditRiskblueprint', models.DO_NOTHING, related_name='AuditRisk_blueprint')
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING, related_name='AuditRisk_engagement')

    class Meta:
        managed = False
        db_table = 'audit_risk'


class AuditRiskblueprint(models.TenantModel):
    order = models.IntegerField()
    weight = models.SmallIntegerField()
    is_key = models.BooleanField()
    header = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('AuditRiskcategory', models.DO_NOTHING, related_name='AuditRiskblueprint_category')

    class Meta:
        managed = False
        db_table = 'audit_riskblueprint'


class AuditRiskcategory(models.TenantModel):
    order = models.IntegerField()
    header = models.CharField(max_length=255)
    category_type = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    parent = models.ForeignKey('self', models.DO_NOTHING, related_name='AuditRiskcategory_parent', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_riskcategory'


class AuditSpecialaudit(models.TenantModel):
    engagement_ptr = models.OneToOneField(AuditEngagement, models.DO_NOTHING, related_name='AuditSpecialaudit_engagement_ptr')

    class Meta:
        managed = False
        db_table = 'audit_specialaudit'


class AuditSpecialauditrecommendation(models.TenantModel):
    description = models.TextField()
    audit = models.ForeignKey(AuditSpecialaudit, models.DO_NOTHING, related_name='AuditSpecialauditrecommendation_audit')

    class Meta:
        managed = False
        db_table = 'audit_specialauditrecommendation'


class AuditSpecificprocedure(models.TenantModel):
    description = models.TextField()
    finding = models.TextField()
    audit = models.ForeignKey(AuditSpecialaudit, models.DO_NOTHING, related_name='AuditSpecificprocedure_audit')

    class Meta:
        managed = False
        db_table = 'audit_specificprocedure'


class AuditSpotcheck(models.TenantModel):
    engagement_ptr = models.OneToOneField(AuditEngagement, models.DO_NOTHING, related_name='AuditSpotcheck_engagement_ptr')
    total_amount_tested = models.DecimalField(max_digits=20, decimal_places=2)
    total_amount_of_ineligible_expenditure = models.DecimalField(max_digits=20, decimal_places=2)
    internal_controls = models.TextField()

    class Meta:
        managed = False
        db_table = 'audit_spotcheck'


class DjangoCommentFlags(models.TenantModel):
    flag = models.CharField(max_length=30)
    flag_date = models.DateTimeField()
    comment = models.ForeignKey('DjangoComments', models.DO_NOTHING, related_name='DjangoCommentFlags_comment')
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='DjangoCommentFlags_user')

    class Meta:
        managed = False
        db_table = 'django_comment_flags'
        unique_together = (('comment', 'flag', 'user'),)


class DjangoComments(models.TenantModel):
    object_pk = models.TextField()
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=254)
    user_url = models.CharField(max_length=200)
    comment = models.TextField()
    submit_date = models.DateTimeField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    is_public = models.BooleanField()
    is_removed = models.BooleanField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='DjangoComments_content_type')
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING, related_name='DjangoComments_site')
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='DjangoComments_user', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_comments'


class FundsDonor(models.TenantModel):
    name = models.CharField(unique=True, max_length=45)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_donor'


class FundsFundscommitmentheader(models.TenantModel):
    vendor_code = models.CharField(max_length=20)
    fc_number = models.CharField(unique=True, max_length=20)
    document_date = models.DateField(blank=True, null=True)
    fc_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    document_text = models.CharField(max_length=255)
    exchange_rate = models.CharField(max_length=20)
    responsible_person = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_fundscommitmentheader'


class FundsFundscommitmentitem(models.TenantModel):
    fc_ref_number = models.CharField(max_length=30)
    line_item = models.CharField(max_length=5)
    wbs = models.CharField(max_length=30)
    grant_number = models.CharField(max_length=20)
    fund = models.CharField(max_length=10)
    gl_account = models.CharField(max_length=15)
    due_date = models.DateField(blank=True, null=True)
    fr_number = models.CharField(max_length=20)
    commitment_amount = models.DecimalField(max_digits=20, decimal_places=2)
    commitment_amount_dc = models.DecimalField(max_digits=20, decimal_places=2)
    amount_changed = models.DecimalField(max_digits=20, decimal_places=2)
    line_item_text = models.CharField(max_length=255)
    fund_commitment = models.ForeignKey(FundsFundscommitmentheader, models.DO_NOTHING, related_name='FundsFundscommitmentitem_fund_commitment')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_fundscommitmentitem'
        unique_together = (('fund_commitment', 'line_item'),)


class FundsFundsreservationheader(models.TenantModel):
    vendor_code = models.CharField(max_length=20)
    fr_number = models.CharField(unique=True, max_length=20)
    document_date = models.DateField(blank=True, null=True)
    fr_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    document_text = models.CharField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    actual_amt = models.DecimalField(max_digits=20, decimal_places=2)
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, related_name='frs', blank=True, null=True)
    intervention_amt = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_amt = models.DecimalField(max_digits=20, decimal_places=2)
    total_amt = models.DecimalField(max_digits=20, decimal_places=2)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    actual_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    total_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    multi_curr_flag = models.BooleanField()
    completed_flag = models.BooleanField()
    delegated = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'funds_fundsreservationheader'
        unique_together = (('fr_number', 'vendor_code'),)


class FundsFundsreservationitem(models.TenantModel):
    fr_ref_number = models.CharField(max_length=30)
    line_item = models.SmallIntegerField()
    wbs = models.CharField(max_length=30)
    grant_number = models.CharField(max_length=20)
    fund = models.CharField(max_length=10)
    overall_amount = models.DecimalField(max_digits=20, decimal_places=2)
    overall_amount_dc = models.DecimalField(max_digits=20, decimal_places=2)
    due_date = models.DateField(blank=True, null=True)
    line_item_text = models.CharField(max_length=255)
    fund_reservation = models.ForeignKey(FundsFundsreservationheader, models.DO_NOTHING, related_name='FundsFundsreservationitem_fund_reservation')
    created = models.DateTimeField()
    modified = models.DateTimeField()
    donor = models.CharField(max_length=256, blank=True, null=True)
    donor_code = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funds_fundsreservationitem'
        unique_together = (('fund_reservation', 'line_item'),)


class FundsGrant(models.TenantModel):
    name = models.CharField(unique=True, max_length=128)
    donor = models.ForeignKey(FundsDonor, models.DO_NOTHING, related_name='FundsGrant_donor')
    expiry = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=255)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_grant'


class HactAggregatehact(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.IntegerField(unique=True)
    partner_values = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'hact_aggregatehact'


class HactHacthistory(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.IntegerField()
    partner_values = models.TextField(blank=True, null=True)  # This field type is a guess.
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='HactHacthistory_partner')

    class Meta:
        managed = False
        db_table = 'hact_hacthistory'
        unique_together = (('partner', 'year'),)


class LocationsCartodbtable(models.TenantModel):
    domain = models.CharField(max_length=254)
    api_key = models.CharField(max_length=254)
    table_name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254)
    name_col = models.CharField(max_length=254)
    pcode_col = models.CharField(max_length=254)
    parent_code_col = models.CharField(max_length=254)
    color = models.CharField(max_length=7)
    location_type = models.ForeignKey('LocationsGatewaytype', models.DO_NOTHING, related_name='LocationsCartodbtable_location_type')
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, related_name='LocationsCartodbtable_parent', blank=True, null=True)
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    remap_table_name = models.CharField(max_length=254, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'locations_cartodbtable'


class LocationsGatewaytype(models.TenantModel):
    name = models.CharField(unique=True, max_length=64)
    admin_level = models.SmallIntegerField(unique=True, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'locations_gatewaytype'


class LocationsLocation(models.TenantModel):
    name = models.CharField(max_length=254)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    p_code = models.CharField(max_length=32)
    point = models.TextField(blank=True, null=True)  # This field type is a guess.
    gateway = models.ForeignKey(LocationsGatewaytype, models.DO_NOTHING, related_name='LocationsLocation_gateway')
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, related_name='LocationsLocation_parent', blank=True, null=True)
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'locations_location'
        unique_together = (('gateway', 'name', 'p_code'),)


class LocationsLocationremaphistory(models.TenantModel):
    comments = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    new_location = models.ForeignKey(LocationsLocation, models.DO_NOTHING, related_name='LocationsLocationremaphistory_new_location')
    old_location = models.ForeignKey(LocationsLocation, models.DO_NOTHING, related_name='LocationsLocationremaphistory_old_location')
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'locations_locationremaphistory'


class PartnersAgreement(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    agreement_type = models.CharField(max_length=10)
    agreement_number = models.CharField(unique=True, max_length=45)
    attached_agreement = models.CharField(max_length=1024)
    signed_by_unicef_date = models.DateField(blank=True, null=True)
    signed_by_partner_date = models.DateField(blank=True, null=True)
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='agreements')
    partner_manager = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, related_name='PartnersAgreement_partner_manager', blank=True, null=True)
    signed_by = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='PartnersAgreement_signed_by', blank=True, null=True)
    status = models.CharField(max_length=32)
    country_programme = models.ForeignKey('ReportsCountryprogramme', models.DO_NOTHING, related_name='PartnersAgreement_country_programme', blank=True, null=True)
    reference_number_year = models.IntegerField()
    special_conditions_pca = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'partners_agreement'


class PartnersAgreementAuthorizedOfficers(models.TenantModel):
    agreement = models.ForeignKey(PartnersAgreement, models.DO_NOTHING, related_name='PartnersAgreementAuthorizedOfficers_agreement')
    partnerstaffmember = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, related_name='PartnersAgreementAuthorizedOfficers_partnerstaffmember')

    class Meta:
        managed = False
        db_table = 'partners_agreement_authorized_officers'
        unique_together = (('agreement', 'partnerstaffmember'),)


class PartnersAgreementamendment(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    number = models.CharField(max_length=5)
    signed_amendment = models.CharField(max_length=1024, blank=True, null=True)
    signed_date = models.DateField(blank=True, null=True)
    agreement = models.ForeignKey(PartnersAgreement, models.DO_NOTHING, related_name='PartnersAgreementamendment_agreement')
    types = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'partners_agreementamendment'


class PartnersAssessment(models.TenantModel):
    type = models.CharField(max_length=50)
    names_of_other_agencies = models.CharField(max_length=255, blank=True, null=True)
    expected_budget = models.IntegerField(blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    requested_date = models.DateField()
    planned_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    rating = models.CharField(max_length=50)
    report = models.CharField(max_length=1024, blank=True, null=True)
    current = models.BooleanField()
    approving_officer = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='PartnersAssessment_approving_officer', blank=True, null=True)
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='PartnersAssessment_partner')
    requesting_officer = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='PartnersAssessment_requesting_officer', blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'partners_assessment'


class PartnersCorevaluesassessment(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    date = models.DateField(blank=True, null=True)
    assessment = models.CharField(max_length=1024, blank=True, null=True)
    archived = models.BooleanField()
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='core_values_assessments')

    class Meta:
        managed = False
        db_table = 'partners_corevaluesassessment'


class PartnersDirectcashtransfer(models.TenantModel):
    fc_ref = models.CharField(max_length=50)
    amount_usd = models.DecimalField(max_digits=20, decimal_places=2)
    liquidation_usd = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_balance_usd = models.DecimalField(max_digits=20, decimal_places=2)
    amount_less_than_3_months_usd = models.DecimalField(db_column='amount_less_than_3_Months_usd', max_digits=20, decimal_places=2)  # Field name made lowercase.
    amount_3_to_6_months_usd = models.DecimalField(max_digits=20, decimal_places=2)
    amount_6_to_9_months_usd = models.DecimalField(max_digits=20, decimal_places=2)
    amount_more_than_9_months_usd = models.DecimalField(db_column='amount_more_than_9_Months_usd', max_digits=20, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'partners_directcashtransfer'


class PartnersFiletype(models.TenantModel):
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        managed = False
        db_table = 'partners_filetype'


class PartnersIntervention(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    document_type = models.CharField(max_length=255)
    number = models.CharField(unique=True, max_length=64, blank=True, null=True)
    title = models.CharField(max_length=256)
    status = models.CharField(max_length=32)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    submission_date_prc = models.DateField(blank=True, null=True)
    review_date_prc = models.DateField(blank=True, null=True)
    prc_review_document = models.CharField(max_length=1024, blank=True, null=True)
    signed_by_unicef_date = models.DateField(blank=True, null=True)
    signed_by_partner_date = models.DateField(blank=True, null=True)
    population_focus = models.CharField(max_length=130, blank=True, null=True)
    agreement = models.ForeignKey(PartnersAgreement, models.DO_NOTHING, related_name='interventions')
    partner_authorized_officer_signatory = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, related_name='PartnersIntervention_partner_authorized_officer_signatory', blank=True, null=True)
    unicef_signatory = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='PartnersIntervention_unicef_signatory', blank=True, null=True)
    signed_pd_document = models.CharField(max_length=1024, blank=True, null=True)
    country_programme = models.ForeignKey('ReportsCountryprogramme', models.DO_NOTHING, related_name='interventions', blank=True, null=True)
    contingency_pd = models.BooleanField()
    metadata = models.TextField(blank=True, null=True)  # This field type is a guess.
    in_amendment = models.BooleanField()
    reference_number_year = models.IntegerField(blank=True, null=True)
    activation_letter = models.CharField(max_length=1024, blank=True, null=True)
    termination_doc = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partners_intervention'


class PartnersInterventionFlatLocations(models.TenantModel):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='PartnersInterventionFlatLocations_intervention')
    location = models.ForeignKey(LocationsLocation, models.DO_NOTHING, related_name='PartnersInterventionFlatLocations_location')

    class Meta:
        managed = False
        db_table = 'partners_intervention_flat_locations'
        unique_together = (('intervention', 'location'),)


class PartnersInterventionOffices(models.TenantModel):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='PartnersInterventionOffices_intervention')
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='PartnersInterventionOffices_office')

    class Meta:
        managed = False
        db_table = 'partners_intervention_offices'
        unique_together = (('intervention', 'office'),)


class PartnersInterventionPartnerFocalPoints(models.TenantModel):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='PartnersInterventionPartnerFocalPoints_intervention')
    partnerstaffmember = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, related_name='PartnersInterventionPartnerFocalPoints_partnerstaffmember')

    class Meta:
        managed = False
        db_table = 'partners_intervention_partner_focal_points'
        unique_together = (('intervention', 'partnerstaffmember'),)


class PartnersInterventionSections(models.TenantModel):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='PartnersInterventionSections_intervention')
    section = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='PartnersInterventionSections_section')

    class Meta:
        managed = False
        db_table = 'partners_intervention_sections'
        unique_together = (('intervention', 'section'),)


class PartnersInterventionUnicefFocalPoints(models.TenantModel):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='PartnersInterventionUnicefFocalPoints_intervention')
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='PartnersInterventionUnicefFocalPoints_user')

    class Meta:
        managed = False
        db_table = 'partners_intervention_unicef_focal_points'
        unique_together = (('intervention', 'user'),)


class PartnersInterventionamendment(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    signed_date = models.DateField(blank=True, null=True)
    amendment_number = models.IntegerField()
    signed_amendment = models.CharField(max_length=1024)
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='PartnersInterventionamendment_intervention')
    types = models.TextField()  # This field type is a guess.
    other_description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partners_interventionamendment'


class PartnersInterventionattachment(models.TenantModel):
    attachment = models.CharField(max_length=1024)
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='attachments')
    type = models.ForeignKey(PartnersFiletype, models.DO_NOTHING, related_name='PartnersInterventionattachment_type')
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'partners_interventionattachment'


class PartnersInterventionbudget(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    partner_contribution = models.DecimalField(max_digits=20, decimal_places=2)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2)
    in_kind_amount = models.DecimalField(max_digits=20, decimal_places=2)
    partner_contribution_local = models.DecimalField(max_digits=20, decimal_places=2)
    unicef_cash_local = models.DecimalField(max_digits=20, decimal_places=2)
    in_kind_amount_local = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    intervention = models.OneToOneField(PartnersIntervention, models.DO_NOTHING, related_name='planned_budget', blank=True, null=True)
    total_local = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'partners_interventionbudget'


class PartnersInterventionplannedvisits(models.TenantModel):
    year = models.IntegerField()
    programmatic_q4 = models.IntegerField()
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='PartnersInterventionplannedvisits_intervention')
    created = models.DateTimeField()
    modified = models.DateTimeField()
    programmatic_q1 = models.IntegerField()
    programmatic_q2 = models.IntegerField()
    programmatic_q3 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'partners_interventionplannedvisits'
        unique_together = (('intervention', 'year'),)


class PartnersInterventionreportingperiod(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    due_date = models.DateField()
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='PartnersInterventionreportingperiod_intervention')

    class Meta:
        managed = False
        db_table = 'partners_interventionreportingperiod'


class PartnersInterventionresultlink(models.TenantModel):
    cp_output = models.ForeignKey('ReportsResult', models.DO_NOTHING, related_name='PartnersInterventionresultlink_cp_output')
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='PartnersInterventionresultlink_intervention')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_interventionresultlink'


class PartnersInterventionresultlinkRamIndicators(models.TenantModel):
    interventionresultlink = models.ForeignKey(PartnersInterventionresultlink, models.DO_NOTHING, related_name='PartnersInterventionresultlinkRamIndicators_interventionresultlink')
    indicator = models.ForeignKey('ReportsIndicator', models.DO_NOTHING, related_name='PartnersInterventionresultlinkRamIndicators_indicator')

    class Meta:
        managed = False
        db_table = 'partners_interventionresultlink_ram_indicators'
        unique_together = (('indicator', 'interventionresultlink'),)


class PartnersPartnerorganization(models.TenantModel):
    partner_type = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    address = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=64, blank=True, null=True)
    vendor_number = models.CharField(unique=True, max_length=30, blank=True, null=True)
    alternate_id = models.IntegerField(blank=True, null=True)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=50, blank=True, null=True)
    core_values_assessment_date = models.DateField(blank=True, null=True)
    cso_type = models.CharField(max_length=50, blank=True, null=True)
    vision_synced = models.BooleanField()
    type_of_assessment = models.CharField(max_length=50, blank=True, null=True)
    last_assessment_date = models.DateField(blank=True, null=True)
    hidden = models.BooleanField()
    deleted_flag = models.BooleanField()
    total_ct_cp = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_ct_cy = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    blocked = models.BooleanField()
    city = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    postal_code = models.CharField(max_length=32, blank=True, null=True)
    shared_with = models.TextField(blank=True, null=True)  # This field type is a guess.
    street_address = models.CharField(max_length=500, blank=True, null=True)
    hact_values = models.TextField(blank=True, null=True)  # This field type is a guess.
    created = models.DateTimeField()
    modified = models.DateTimeField()
    net_ct_cy = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    reported_cy = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_ct_ytd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    basis_for_risk_rating = models.CharField(max_length=50)
    manually_blocked = models.BooleanField()
    outstanding_dct_amount_6_to_9_months_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    outstanding_dct_amount_more_than_9_months_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partners_partnerorganization'
        unique_together = (('name', 'vendor_number'),)


class PartnersPartnerplannedvisits(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.IntegerField()
    programmatic_q1 = models.IntegerField()
    programmatic_q2 = models.IntegerField()
    programmatic_q3 = models.IntegerField()
    programmatic_q4 = models.IntegerField()
    partner = models.ForeignKey(PartnersPartnerorganization, models.DO_NOTHING, related_name='PartnersPartnerplannedvisits_partner')

    class Meta:
        managed = False
        db_table = 'partners_partnerplannedvisits'
        unique_together = (('partner', 'year'),)


class PartnersPartnerstaffmember(models.TenantModel):
    title = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(unique=True, max_length=128)
    phone = models.CharField(max_length=64, blank=True, null=True)
    partner = models.ForeignKey(PartnersPartnerorganization, models.DO_NOTHING, related_name='PartnersPartnerstaffmember_partner')
    active = models.BooleanField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_partnerstaffmember'


class PartnersPlannedengagement(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    spot_check_planned_q1 = models.IntegerField()
    spot_check_planned_q2 = models.IntegerField()
    spot_check_planned_q3 = models.IntegerField()
    spot_check_planned_q4 = models.IntegerField()
    scheduled_audit = models.BooleanField()
    special_audit = models.BooleanField()
    partner = models.OneToOneField(PartnersPartnerorganization, models.DO_NOTHING, related_name='PartnersPlannedengagement_partner')
    spot_check_follow_up = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'partners_plannedengagement'


class PartnersWorkspacefiletype(models.TenantModel):
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        managed = False
        db_table = 'partners_workspacefiletype'


class ReportsAppliedindicator(models.TenantModel):
    context_code = models.CharField(max_length=50, blank=True, null=True)
    assumptions = models.TextField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    indicator = models.ForeignKey('ReportsIndicatorblueprint', models.DO_NOTHING, related_name='ReportsAppliedindicator_indicator', blank=True, null=True)
    lower_result = models.ForeignKey('ReportsLowerresult', models.DO_NOTHING, related_name='ReportsAppliedindicator_lower_result')
    means_of_verification = models.CharField(max_length=255, blank=True, null=True)
    cluster_indicator_id = models.IntegerField(blank=True, null=True)
    cluster_indicator_title = models.CharField(max_length=1024, blank=True, null=True)
    cluster_name = models.CharField(max_length=512, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    response_plan_name = models.CharField(max_length=1024, blank=True, null=True)
    section = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='ReportsAppliedindicator_section', blank=True, null=True)
    is_active = models.BooleanField()
    is_high_frequency = models.BooleanField()
    baseline = models.TextField(blank=True, null=True)  # This field type is a guess.
    denominator_label = models.CharField(max_length=256, blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    measurement_specifications = models.TextField(blank=True, null=True)
    numerator_label = models.CharField(max_length=256, blank=True, null=True)
    target = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'reports_appliedindicator'
        unique_together = (('indicator', 'lower_result'),)


class ReportsAppliedindicatorDisaggregation(models.TenantModel):
    appliedindicator = models.ForeignKey(ReportsAppliedindicator, models.DO_NOTHING, related_name='ReportsAppliedindicatorDisaggregation_appliedindicator')
    disaggregation = models.ForeignKey('ReportsDisaggregation', models.DO_NOTHING, related_name='ReportsAppliedindicatorDisaggregation_disaggregation')

    class Meta:
        managed = False
        db_table = 'reports_appliedindicator_disaggregation'
        unique_together = (('appliedindicator', 'disaggregation'),)


class ReportsAppliedindicatorLocations(models.TenantModel):
    appliedindicator = models.ForeignKey(ReportsAppliedindicator, models.DO_NOTHING, related_name='ReportsAppliedindicatorLocations_appliedindicator')
    location = models.ForeignKey(LocationsLocation, models.DO_NOTHING, related_name='ReportsAppliedindicatorLocations_location')

    class Meta:
        managed = False
        db_table = 'reports_appliedindicator_locations'
        unique_together = (('appliedindicator', 'location'),)


class ReportsCountryprogramme(models.TenantModel):
    name = models.CharField(max_length=150)
    wbs = models.CharField(unique=True, max_length=30)
    from_date = models.DateField()
    to_date = models.DateField()
    invalid = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'reports_countryprogramme'


class ReportsDisaggregation(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'reports_disaggregation'


class ReportsDisaggregationvalue(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    value = models.CharField(max_length=15)
    active = models.BooleanField()
    disaggregation = models.ForeignKey(ReportsDisaggregation, models.DO_NOTHING, related_name='ReportsDisaggregationvalue_disaggregation')

    class Meta:
        managed = False
        db_table = 'reports_disaggregationvalue'


class ReportsIndicator(models.TenantModel):
    name = models.CharField(max_length=1024)
    code = models.CharField(max_length=50, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    sector_total = models.IntegerField(blank=True, null=True)
    current = models.IntegerField(blank=True, null=True)
    sector_current = models.IntegerField(blank=True, null=True)
    view_on_dashboard = models.BooleanField()
    result = models.ForeignKey('ReportsResult', models.DO_NOTHING, related_name='ReportsIndicator_result', blank=True, null=True)
    sector = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='ReportsIndicator_sector', blank=True, null=True)
    unit = models.ForeignKey('ReportsUnit', models.DO_NOTHING, related_name='ReportsIndicator_unit', blank=True, null=True)
    baseline = models.CharField(max_length=255, blank=True, null=True)
    ram_indicator = models.BooleanField()
    target = models.CharField(max_length=255, blank=True, null=True)
    assumptions = models.TextField(blank=True, null=True)
    active = models.BooleanField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_indicator'
        unique_together = (('name', 'result', 'sector'),)


class ReportsIndicatorblueprint(models.TenantModel):
    title = models.CharField(max_length=1024)
    description = models.CharField(max_length=3072, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)
    subdomain = models.CharField(max_length=255, blank=True, null=True)
    disaggregatable = models.BooleanField()
    unit = models.CharField(max_length=10)
    calculation_formula_across_locations = models.CharField(max_length=10)
    calculation_formula_across_periods = models.CharField(max_length=10)
    created = models.DateTimeField()
    display_type = models.CharField(max_length=10)
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_indicatorblueprint'


class ReportsLowerresult(models.TenantModel):
    name = models.CharField(max_length=500)
    code = models.CharField(max_length=50)
    result_link = models.ForeignKey(PartnersInterventionresultlink, models.DO_NOTHING, related_name='ReportsLowerresult_result_link')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_lowerresult'
        unique_together = (('code', 'result_link'),)


class ReportsQuarter(models.TenantModel):
    name = models.CharField(max_length=64)
    year = models.CharField(max_length=4)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_quarter'


class ReportsReportingrequirement(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    due_date = models.DateField()
    report_type = models.CharField(max_length=50)
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='ReportsReportingrequirement_intervention')

    class Meta:
        managed = False
        db_table = 'reports_reportingrequirement'


class ReportsResult(models.TenantModel):
    name = models.TextField()
    code = models.CharField(max_length=50, blank=True, null=True)
    result_type = models.ForeignKey('ReportsResulttype', models.DO_NOTHING, related_name='ReportsResult_result_type')
    sector = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='ReportsResult_sector', blank=True, null=True)
    gic_code = models.CharField(max_length=8, blank=True, null=True)
    gic_name = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_tag = models.BooleanField()
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, related_name='ReportsResult_parent', blank=True, null=True)
    rght = models.IntegerField()
    sic_code = models.CharField(max_length=8, blank=True, null=True)
    sic_name = models.CharField(max_length=255, blank=True, null=True)
    tree_id = models.IntegerField()
    vision_id = models.CharField(max_length=10, blank=True, null=True)
    wbs = models.CharField(max_length=50, blank=True, null=True)
    activity_focus_code = models.CharField(max_length=8, blank=True, null=True)
    activity_focus_name = models.CharField(max_length=255, blank=True, null=True)
    hidden = models.BooleanField()
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    ram = models.BooleanField()
    country_programme = models.ForeignKey(ReportsCountryprogramme, models.DO_NOTHING, related_name='ReportsResult_country_programme', blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    humanitarian_marker_code = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_marker_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reports_result'
        unique_together = (('country_programme', 'wbs'),)


class ReportsResulttype(models.TenantModel):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'reports_resulttype'


class ReportsSector(models.TenantModel):
    name = models.CharField(unique=True, max_length=45)
    description = models.CharField(max_length=256, blank=True, null=True)
    alternate_id = models.IntegerField(blank=True, null=True)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    dashboard = models.BooleanField()
    color = models.CharField(max_length=7, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_sector'


class ReportsSpecialreportingrequirement(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    description = models.CharField(max_length=256)
    due_date = models.DateField()
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='ReportsSpecialreportingrequirement_intervention')

    class Meta:
        managed = False
        db_table = 'reports_specialreportingrequirement'


class ReportsUnit(models.TenantModel):
    type = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'reports_unit'


class SnapshotActivity(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    target_object_id = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
    data = models.TextField()  # This field type is a guess.
    change = models.TextField()  # This field type is a guess.
    by_user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='SnapshotActivity_by_user')
    target_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='SnapshotActivity_target_content_type')

    class Meta:
        managed = False
        db_table = 'snapshot_activity'


class T2FItineraryitem(models.TenantModel):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    overnight_travel = models.BooleanField()
    mode_of_travel = models.CharField(max_length=5)
    dsa_region = models.ForeignKey('PublicsDsaregion', models.DO_NOTHING, related_name='T2FItineraryitem_dsa_region', blank=True, null=True)
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING, related_name='T2FItineraryitem_travel')
    field_order = models.IntegerField(db_column='_order')  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 't2f_itineraryitem'


class T2FItineraryitemAirlines(models.TenantModel):
    itineraryitem = models.ForeignKey(T2FItineraryitem, models.DO_NOTHING, related_name='T2FItineraryitemAirlines_itineraryitem')
    airlinecompany = models.ForeignKey('PublicsAirlinecompany', models.DO_NOTHING, related_name='T2FItineraryitemAirlines_airlinecompany')

    class Meta:
        managed = False
        db_table = 't2f_itineraryitem_airlines'
        unique_together = (('airlinecompany', 'itineraryitem'),)


class T2FTravel(models.TenantModel):
    created = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    rejection_note = models.TextField()
    cancellation_note = models.TextField()
    certification_note = models.TextField()
    report_note = models.TextField()
    misc_expenses = models.TextField()
    status = models.CharField(max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    purpose = models.CharField(max_length=500)
    additional_note = models.TextField()
    international_travel = models.NullBooleanField()
    ta_required = models.NullBooleanField()
    reference_number = models.CharField(unique=True, max_length=12)
    hidden = models.BooleanField()
    mode_of_travel = models.TextField(blank=True, null=True)  # This field type is a guess.
    estimated_travel_cost = models.DecimalField(max_digits=20, decimal_places=4)
    is_driver = models.BooleanField()
    preserved_expenses_local = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    approved_cost_traveler = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    approved_cost_travel_agencies = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, related_name='T2FTravel_currency', blank=True, null=True)
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='T2FTravel_office', blank=True, null=True)
    supervisor = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='T2FTravel_supervisor', blank=True, null=True)
    traveler = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='T2FTravel_traveler', blank=True, null=True)
    first_submission_date = models.DateTimeField(blank=True, null=True)
    preserved_expenses_usd = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    section = models.ForeignKey(ReportsSector, models.DO_NOTHING, related_name='T2FTravel_section', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_travel'


class T2FTravelactivity(models.TenantModel):
    travel_type = models.CharField(max_length=64)
    date = models.DateField(blank=True, null=True)
    partner = models.ForeignKey(PartnersPartnerorganization, models.DO_NOTHING, related_name='+', blank=True, null=True)
    partnership = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='travel_activities', blank=True, null=True)
    primary_traveler = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='T2FTravelactivity_primary_traveler')
    result = models.ForeignKey(ReportsResult, models.DO_NOTHING, related_name='T2FTravelactivity_result', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_travelactivity'


class T2FTravelactivityLocations(models.TenantModel):
    travelactivity = models.ForeignKey(T2FTravelactivity, models.DO_NOTHING, related_name='T2FTravelactivityLocations_travelactivity')
    location = models.ForeignKey(LocationsLocation, models.DO_NOTHING, related_name='T2FTravelactivityLocations_location')

    class Meta:
        managed = False
        db_table = 't2f_travelactivity_locations'
        unique_together = (('location', 'travelactivity'),)


class T2FTravelactivityTravels(models.TenantModel):
    travelactivity = models.ForeignKey(T2FTravelactivity, models.DO_NOTHING, related_name='T2FTravelactivityTravels_travelactivity')
    travel = models.ForeignKey(T2FTravel, models.DO_NOTHING, related_name='T2FTravelactivityTravels_travel')

    class Meta:
        managed = False
        db_table = 't2f_travelactivity_travels'
        unique_together = (('travel', 'travelactivity'),)


class T2FTravelattachment(models.TenantModel):
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    file = models.CharField(max_length=255, blank=True, null=True)
    travel = models.ForeignKey(T2FTravel, models.DO_NOTHING, related_name='attachments')

    class Meta:
        managed = False
        db_table = 't2f_travelattachment'


class TpmTpmactivity(models.TenantModel):
    activity_ptr = models.OneToOneField(ActivitiesActivity, models.DO_NOTHING, related_name='TpmTpmactivity_activity_ptr')
    additional_information = models.TextField()
    is_pv = models.BooleanField()
    tpm_visit = models.ForeignKey('TpmTpmvisit', models.DO_NOTHING, related_name='TpmTpmactivity_tpm_visit')
    section = models.ForeignKey(ReportsSector, models.DO_NOTHING, related_name='TpmTpmactivity_section')

    class Meta:
        managed = False
        db_table = 'tpm_tpmactivity'


class TpmTpmactivityOffices(models.TenantModel):
    tpmactivity = models.ForeignKey(TpmTpmactivity, models.DO_NOTHING, related_name='TpmTpmactivityOffices_tpmactivity')
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='TpmTpmactivityOffices_office')

    class Meta:
        managed = False
        db_table = 'tpm_tpmactivity_offices'
        unique_together = (('office', 'tpmactivity'),)


class TpmTpmactivityUnicefFocalPoints(models.TenantModel):
    tpmactivity = models.ForeignKey(TpmTpmactivity, models.DO_NOTHING, related_name='TpmTpmactivityUnicefFocalPoints_tpmactivity')
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='TpmTpmactivityUnicefFocalPoints_user')

    class Meta:
        managed = False
        db_table = 'tpm_tpmactivity_unicef_focal_points'
        unique_together = (('tpmactivity', 'user'),)


class TpmTpmvisit(models.TenantModel):
    deleted_at = models.DateTimeField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=20)
    reject_comment = models.TextField()
    approval_comment = models.TextField()
    visit_information = models.TextField()
    date_of_assigned = models.DateField(blank=True, null=True)
    date_of_cancelled = models.DateField(blank=True, null=True)
    date_of_tpm_accepted = models.DateField(blank=True, null=True)
    date_of_tpm_rejected = models.DateField(blank=True, null=True)
    date_of_tpm_reported = models.DateField(blank=True, null=True)
    date_of_tpm_report_rejected = models.DateField(blank=True, null=True)
    date_of_unicef_approved = models.DateField(blank=True, null=True)
    tpm_partner = models.ForeignKey('TpmpartnersTpmpartner', models.DO_NOTHING, related_name='TpmTpmvisit_tpm_partner', blank=True, null=True)
    cancel_comment = models.TextField()
    author = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='TpmTpmvisit_author', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tpm_tpmvisit'


class TpmTpmvisitTpmPartnerFocalPoints(models.TenantModel):
    tpmvisit = models.ForeignKey(TpmTpmvisit, models.DO_NOTHING, related_name='TpmTpmvisitTpmPartnerFocalPoints_tpmvisit')
    tpmpartnerstaffmember = models.ForeignKey('TpmpartnersTpmpartnerstaffmember', models.DO_NOTHING, related_name='TpmTpmvisitTpmPartnerFocalPoints_tpmpartnerstaffmember')

    class Meta:
        managed = False
        db_table = 'tpm_tpmvisit_tpm_partner_focal_points'
        unique_together = (('tpmpartnerstaffmember', 'tpmvisit'),)


class TpmTpmvisitreportrejectcomment(models.TenantModel):
    rejected_at = models.DateTimeField()
    reject_reason = models.TextField()
    tpm_visit = models.ForeignKey(TpmTpmvisit, models.DO_NOTHING, related_name='TpmTpmvisitreportrejectcomment_tpm_visit')

    class Meta:
        managed = False
        db_table = 'tpm_tpmvisitreportrejectcomment'


class UnicefAttachmentsAttachment(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    file = models.CharField(max_length=1024, blank=True, null=True)
    hyperlink = models.CharField(max_length=255)
    object_id = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=64)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='UnicefAttachmentsAttachment_content_type', blank=True, null=True)
    file_type = models.ForeignKey('UnicefAttachmentsFiletype', models.DO_NOTHING, related_name='UnicefAttachmentsAttachment_file_type', blank=True, null=True)
    uploaded_by = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='UnicefAttachmentsAttachment_uploaded_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_attachments_attachment'


class UnicefAttachmentsAttachmentflat(models.TenantModel):
    object_link = models.CharField(max_length=200)
    file_type = models.CharField(max_length=100)
    file_link = models.CharField(max_length=1024)
    filename = models.CharField(max_length=1024)
    uploaded_by = models.CharField(max_length=255)
    created = models.CharField(max_length=50)
    attachment = models.ForeignKey(UnicefAttachmentsAttachment, models.DO_NOTHING, related_name='UnicefAttachmentsAttachmentflat_attachment')

    class Meta:
        managed = False
        db_table = 'unicef_attachments_attachmentflat'


class UnicefAttachmentsAttachmentlink(models.TenantModel):
    object_id = models.IntegerField(blank=True, null=True)
    attachment = models.ForeignKey(UnicefAttachmentsAttachment, models.DO_NOTHING, related_name='UnicefAttachmentsAttachmentlink_attachment')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='UnicefAttachmentsAttachmentlink_content_type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unicef_attachments_attachmentlink'


class UnicefAttachmentsFiletype(models.TenantModel):
    order = models.IntegerField()
    name = models.CharField(max_length=64)
    label = models.CharField(max_length=64)
    code = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'unicef_attachments_filetype'
        unique_together = (('code', 'name'),)


class UnicefSnapshotActivity(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    target_object_id = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
    data = models.TextField()  # This field type is a guess.
    change = models.TextField()  # This field type is a guess.
    by_user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='UnicefSnapshotActivity_by_user')
    target_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='UnicefSnapshotActivity_target_content_type')

    class Meta:
        managed = False
        db_table = 'unicef_snapshot_activity'
