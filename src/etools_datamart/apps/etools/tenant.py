# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ActionPointsActionpoint(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=10)
    description = models.TextField()
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=10)
    action_taken = models.TextField()
    date_of_completion = models.DateTimeField(blank=True, null=True)
    assigned_by = models.ForeignKey('AuthUser', models.DO_NOTHING)
    assigned_to = models.ForeignKey('AuthUser', models.DO_NOTHING)
    author = models.ForeignKey('AuthUser', models.DO_NOTHING)
    cp_output = models.ForeignKey('ReportsResult', models.DO_NOTHING, blank=True, null=True)
    engagement = models.ForeignKey('AuditEngagement', models.DO_NOTHING, blank=True, null=True)
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, blank=True, null=True)
    location = models.ForeignKey('LocationsLocation', models.DO_NOTHING, blank=True, null=True)
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING)
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, blank=True, null=True)
    section = models.ForeignKey('ReportsSector', models.DO_NOTHING)
    tpm_activity = models.ForeignKey('TpmTpmactivity', models.DO_NOTHING, blank=True, null=True)
    travel_activity = models.ForeignKey('T2FTravelactivity', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action_points_actionpoint'
        unique_together = (('id'),)


class ActivitiesActivity(models.Model):
    date = models.DateField(blank=True, null=True)
    cp_output = models.ForeignKey('ReportsResult', models.DO_NOTHING, blank=True, null=True)
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, blank=True, null=True)
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activities_activity'
        unique_together = (('id'),)


class ActivitiesActivityLocations(models.Model):
    activity = models.ForeignKey(ActivitiesActivity, models.DO_NOTHING)
    location = models.ForeignKey('LocationsLocation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'activities_activity_locations'
        unique_together = (('id'), ('activity', 'location'),)


class ActstreamAction(models.Model):
    actor_object_id = models.CharField(max_length=255)
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    public = models.BooleanField()
    data = models.TextField(blank=True, null=True)
    action_object_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    actor_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    target_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actstream_action'
        unique_together = (('id'),)


class ActstreamFollow(models.Model):
    object_id = models.CharField(max_length=255)
    actor_only = models.BooleanField()
    started = models.DateTimeField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'actstream_follow'
        unique_together = (('id'), ('object_id', 'user', 'content_type'),)


class AttachmentsAttachment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    file = models.CharField(max_length=1024, blank=True, null=True)
    hyperlink = models.CharField(max_length=255)
    object_id = models.IntegerField()
    code = models.CharField(max_length=64)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    file_type = models.ForeignKey('AttachmentsFiletype', models.DO_NOTHING)
    uploaded_by = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attachments_attachment'
        unique_together = (('id'),)


class AttachmentsAttachmentflat(models.Model):
    partner = models.CharField(max_length=255)
    partner_type = models.CharField(max_length=150)
    vendor_number = models.CharField(max_length=50)
    pd_ssfa_number = models.CharField(max_length=64)
    file_type = models.CharField(max_length=100)
    file_link = models.CharField(max_length=1024)
    uploaded_by = models.CharField(max_length=255)
    created = models.CharField(max_length=50)
    attachment = models.ForeignKey(AttachmentsAttachment, models.DO_NOTHING)
    filename = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'attachments_attachmentflat'
        unique_together = (('id'),)


class AttachmentsFiletype(models.Model):
    order = models.IntegerField()
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    label = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'attachments_filetype'
        unique_together = (('id'), ('name', 'code'),)


class AuditAudit(models.Model):
    engagement_ptr = models.ForeignKey('AuditEngagement', models.DO_NOTHING, primary_key=True)
    audited_expenditure = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    financial_findings = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    audit_opinion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'audit_audit'
        unique_together = (('engagement_ptr'),)


class AuditDetailedfindinginfo(models.Model):
    finding = models.TextField()
    recommendation = models.TextField()
    micro_assesment = models.ForeignKey('AuditMicroassessment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_detailedfindinginfo'
        unique_together = (('id'),)


class AuditEngagement(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=30)
    partner_contacted_at = models.DateField(blank=True, null=True)
    engagement_type = models.CharField(max_length=10)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    total_value = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    date_of_field_visit = models.DateField(blank=True, null=True)
    date_of_draft_report_to_ip = models.DateField(blank=True, null=True)
    date_of_comments_by_ip = models.DateField(blank=True, null=True)
    date_of_draft_report_to_unicef = models.DateField(blank=True, null=True)
    date_of_comments_by_unicef = models.DateField(blank=True, null=True)
    date_of_report_submit = models.DateField(blank=True, null=True)
    date_of_final_report = models.DateField(blank=True, null=True)
    date_of_cancel = models.DateField(blank=True, null=True)
    amount_refunded = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    additional_supporting_documentation_provided = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    justification_provided_and_accepted = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    write_off_required = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    cancel_comment = models.TextField()
    explanation_for_additional_information = models.TextField()
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING)
    joint_audit = models.BooleanField()
    agreement = models.ForeignKey('PurchaseOrderPurchaseorder', models.DO_NOTHING)
    po_item = models.ForeignKey('PurchaseOrderPurchaseorderitem', models.DO_NOTHING, blank=True, null=True)
    shared_ip_with = models.TextField()  # This field type is a guess.
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_engagement'
        unique_together = (('id'),)


class AuditEngagementActivePd(models.Model):
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING)
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_engagement_active_pd'
        unique_together = (('engagement', 'intervention'), ('id'),)


class AuditEngagementAuthorizedOfficers(models.Model):
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING)
    partnerstaffmember = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_engagement_authorized_officers'
        unique_together = (('id'), ('engagement', 'partnerstaffmember'),)


class AuditEngagementStaffMembers(models.Model):
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING)
    auditorstaffmember = models.ForeignKey('PurchaseOrderAuditorstaffmember', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_engagement_staff_members'
        unique_together = (('id'), ('auditorstaffmember', 'engagement'),)


class AuditEngagementactionpoint(models.Model):
    category = models.CharField(max_length=100)
    due_date = models.DateField()
    description = models.TextField()
    author = models.ForeignKey('AuthUser', models.DO_NOTHING)
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING)
    person_responsible = models.ForeignKey('AuthUser', models.DO_NOTHING)
    action_taken = models.TextField()
    status = models.CharField(max_length=10)
    high_priority = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'audit_engagementactionpoint'
        unique_together = (('id'),)


class AuditFinancialfinding(models.Model):
    title = models.CharField(max_length=255)
    local_amount = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    recommendation = models.TextField()
    ip_comments = models.TextField()
    audit = models.ForeignKey(AuditAudit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_financialfinding'
        unique_together = (('id'),)


class AuditFinding(models.Model):
    priority = models.CharField(max_length=4)
    category_of_observation = models.CharField(max_length=100)
    recommendation = models.TextField()
    agreed_action_by_ip = models.TextField()
    deadline_of_action = models.DateField(blank=True, null=True)
    spot_check = models.ForeignKey('AuditSpotcheck', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_finding'
        unique_together = (('id'),)


class AuditKeyinternalcontrol(models.Model):
    recommendation = models.TextField()
    audit_observation = models.TextField()
    ip_response = models.TextField()
    audit = models.ForeignKey(AuditAudit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_keyinternalcontrol'
        unique_together = (('id'),)


class AuditMicroassessment(models.Model):
    engagement_ptr = models.ForeignKey(AuditEngagement, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'audit_microassessment'
        unique_together = (('engagement_ptr'),)


class AuditRisk(models.Model):
    value = models.SmallIntegerField(blank=True, null=True)
    extra = models.TextField(blank=True, null=True)  # This field type is a guess.
    blueprint = models.ForeignKey('AuditRiskblueprint', models.DO_NOTHING)
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_risk'
        unique_together = (('engagement', 'blueprint'), ('id'),)


class AuditRiskblueprint(models.Model):
    order = models.IntegerField()
    weight = models.SmallIntegerField()
    is_key = models.BooleanField()
    header = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('AuditRiskcategory', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_riskblueprint'
        unique_together = (('id'),)


class AuditRiskcategory(models.Model):
    order = models.IntegerField()
    header = models.CharField(max_length=255)
    category_type = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_riskcategory'
        unique_together = (('id'),)


class AuditSpecialaudit(models.Model):
    engagement_ptr = models.ForeignKey(AuditEngagement, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'audit_specialaudit'
        unique_together = (('engagement_ptr'),)


class AuditSpecialauditrecommendation(models.Model):
    description = models.TextField()
    audit = models.ForeignKey(AuditSpecialaudit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_specialauditrecommendation'
        unique_together = (('id'),)


class AuditSpecificprocedure(models.Model):
    description = models.TextField()
    finding = models.TextField()
    audit = models.ForeignKey(AuditSpecialaudit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_specificprocedure'
        unique_together = (('id'),)


class AuditSpotcheck(models.Model):
    engagement_ptr = models.ForeignKey(AuditEngagement, models.DO_NOTHING, primary_key=True)
    total_amount_tested = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_amount_of_ineligible_expenditure = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    internal_controls = models.TextField()

    class Meta:
        managed = False
        db_table = 'audit_spotcheck'
        unique_together = (('engagement_ptr'),)


class DjangoCommentFlags(models.Model):
    flag = models.CharField(max_length=30)
    flag_date = models.DateTimeField()
    comment = models.ForeignKey('DjangoComments', models.DO_NOTHING)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_comment_flags'
        unique_together = (('flag', 'user', 'comment'), ('id'),)


class DjangoComments(models.Model):
    object_pk = models.TextField()
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=254)
    user_url = models.CharField(max_length=200)
    comment = models.TextField()
    submit_date = models.DateTimeField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    is_public = models.BooleanField()
    is_removed = models.BooleanField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_comments'
        unique_together = (('id'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class FundsDonor(models.Model):
    name = models.CharField(max_length=45)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_donor'
        unique_together = (('name'), ('id'),)


class FundsFundscommitmentheader(models.Model):
    vendor_code = models.CharField(max_length=20)
    fc_number = models.CharField(max_length=20)
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
        unique_together = (('id'), ('fc_number'),)


class FundsFundscommitmentitem(models.Model):
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
    fund_commitment = models.ForeignKey(FundsFundscommitmentheader, models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_fundscommitmentitem'
        unique_together = (('id'), ('line_item', 'fund_commitment'),)


class FundsFundsreservationheader(models.Model):
    vendor_code = models.CharField(max_length=20)
    fr_number = models.CharField(max_length=20)
    document_date = models.DateField(blank=True, null=True)
    fr_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    document_text = models.CharField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    actual_amt = models.DecimalField(max_digits=20, decimal_places=2)
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, blank=True, null=True)
    intervention_amt = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_amt = models.DecimalField(max_digits=20, decimal_places=2)
    total_amt = models.DecimalField(max_digits=20, decimal_places=2)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    actual_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    total_amt_local = models.DecimalField(max_digits=20, decimal_places=2)
    multi_curr_flag = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'funds_fundsreservationheader'
        unique_together = (('id'), ('vendor_code', 'fr_number'), ('fr_number'),)


class FundsFundsreservationitem(models.Model):
    fr_ref_number = models.CharField(max_length=30)
    line_item = models.CharField(max_length=5)
    wbs = models.CharField(max_length=30)
    grant_number = models.CharField(max_length=20)
    fund = models.CharField(max_length=10)
    overall_amount = models.DecimalField(max_digits=20, decimal_places=2)
    overall_amount_dc = models.DecimalField(max_digits=20, decimal_places=2)
    due_date = models.DateField(blank=True, null=True)
    line_item_text = models.CharField(max_length=255)
    fund_reservation = models.ForeignKey(FundsFundsreservationheader, models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_fundsreservationitem'
        unique_together = (('line_item', 'fund_reservation'), ('id'),)


class FundsGrant(models.Model):
    name = models.CharField(max_length=128)
    donor = models.ForeignKey(FundsDonor, models.DO_NOTHING)
    expiry = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=255)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_grant'
        unique_together = (('name'), ('id'),)


class HactAggregatehact(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.IntegerField()
    partner_values = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'hact_aggregatehact'
        unique_together = (('year'), ('id'),)


class HactHacthistory(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.IntegerField()
    partner_values = models.TextField(blank=True, null=True)  # This field type is a guess.
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hact_hacthistory'
        unique_together = (('id'), ('partner', 'year'),)


class LocationsCartodbtable(models.Model):
    domain = models.CharField(max_length=254)
    api_key = models.CharField(max_length=254)
    table_name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254)
    name_col = models.CharField(max_length=254)
    pcode_col = models.CharField(max_length=254)
    parent_code_col = models.CharField(max_length=254)
    color = models.CharField(max_length=7)
    location_type = models.ForeignKey('LocationsGatewaytype', models.DO_NOTHING)
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    rght = models.IntegerField()
    tree_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'locations_cartodbtable'
        unique_together = (('id'),)


class LocationsGatewaytype(models.Model):
    name = models.CharField(max_length=64)
    admin_level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locations_gatewaytype'
        unique_together = (('admin_level'), ('id'), ('name'),)


class LocationsLocation(models.Model):
    name = models.CharField(max_length=254)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    p_code = models.CharField(max_length=32)
    point = models.GeometryField(blank=True, null=True)
    gateway = models.ForeignKey(LocationsGatewaytype, models.DO_NOTHING)
    geom = models.GeometryField(blank=True, null=True)
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'locations_location'
        unique_together = (('id'), ('name', 'gateway', 'p_code'),)


class ManagementFlaggedissue(models.Model):
    object_id = models.IntegerField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    issue_category = models.CharField(max_length=32)
    issue_id = models.CharField(max_length=100)
    message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    issue_status = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'management_flaggedissue'
        unique_together = (('id'),)


class PartnersAgreement(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    agreement_type = models.CharField(max_length=10)
    agreement_number = models.CharField(max_length=45)
    attached_agreement = models.CharField(max_length=1024)
    signed_by_unicef_date = models.DateField(blank=True, null=True)
    signed_by_partner_date = models.DateField(blank=True, null=True)
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING)
    partner_manager = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, blank=True, null=True)
    signed_by = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=32)
    country_programme = models.ForeignKey('ReportsCountryprogramme', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partners_agreement'
        unique_together = (('agreement_number'), ('id'),)


class PartnersAgreementAuthorizedOfficers(models.Model):
    agreement = models.ForeignKey(PartnersAgreement, models.DO_NOTHING)
    partnerstaffmember = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'partners_agreement_authorized_officers'
        unique_together = (('agreement', 'partnerstaffmember'), ('id'),)


class PartnersAgreementamendment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    number = models.CharField(max_length=5)
    signed_amendment = models.CharField(max_length=1024, blank=True, null=True)
    signed_date = models.DateField(blank=True, null=True)
    agreement = models.ForeignKey(PartnersAgreement, models.DO_NOTHING)
    types = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'partners_agreementamendment'
        unique_together = (('id'),)


class PartnersAssessment(models.Model):
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
    approving_officer = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING)
    requesting_officer = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_assessment'
        unique_together = (('id'),)


class PartnersDirectcashtransfer(models.Model):
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
        unique_together = (('id'),)


class PartnersFiletype(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'partners_filetype'
        unique_together = (('name'), ('id'),)


class PartnersFundingcommitment(models.Model):
    fr_number = models.CharField(max_length=50)
    wbs = models.CharField(max_length=50)
    fc_type = models.CharField(max_length=50)
    fc_ref = models.CharField(max_length=50, blank=True, null=True)
    fr_item_amount_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    agreement_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    commitment_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    expenditure_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    grant = models.ForeignKey(FundsGrant, models.DO_NOTHING, blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partners_fundingcommitment'
        unique_together = (('id'), ('fc_ref'),)


class PartnersIntervention(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    document_type = models.CharField(max_length=255)
    number = models.CharField(max_length=64, blank=True, null=True)
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
    agreement = models.ForeignKey(PartnersAgreement, models.DO_NOTHING)
    partner_authorized_officer_signatory = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, blank=True, null=True)
    unicef_signatory = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    signed_pd_document = models.CharField(max_length=1024, blank=True, null=True)
    country_programme = models.ForeignKey('ReportsCountryprogramme', models.DO_NOTHING, blank=True, null=True)
    contingency_pd = models.BooleanField()
    metadata = models.TextField(blank=True, null=True)  # This field type is a guess.
    in_amendment = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'partners_intervention'
        unique_together = (('id'), ('number'),)


class PartnersInterventionFlatLocations(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)
    location = models.ForeignKey(LocationsLocation, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'partners_intervention_flat_locations'
        unique_together = (('id'), ('intervention', 'location'),)


class PartnersInterventionOffices(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'partners_intervention_offices'
        unique_together = (('id'), ('office', 'intervention'),)


class PartnersInterventionPartnerFocalPoints(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)
    partnerstaffmember = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'partners_intervention_partner_focal_points'
        unique_together = (('intervention', 'partnerstaffmember'), ('id'),)


class PartnersInterventionSections(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)
    sector = models.ForeignKey('ReportsSector', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'partners_intervention_sections'
        unique_together = (('id'), ('sector', 'intervention'),)


class PartnersInterventionUnicefFocalPoints(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'partners_intervention_unicef_focal_points'
        unique_together = (('user', 'intervention'), ('id'),)


class PartnersInterventionamendment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    signed_date = models.DateField(blank=True, null=True)
    amendment_number = models.IntegerField()
    signed_amendment = models.CharField(max_length=1024)
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)
    types = models.TextField()  # This field type is a guess.
    other_description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partners_interventionamendment'
        unique_together = (('id'),)


class PartnersInterventionattachment(models.Model):
    attachment = models.CharField(max_length=1024)
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)
    type = models.ForeignKey(PartnersFiletype, models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_interventionattachment'
        unique_together = (('id'),)


class PartnersInterventionbudget(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    partner_contribution = models.DecimalField(max_digits=20, decimal_places=2)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2)
    in_kind_amount = models.DecimalField(max_digits=20, decimal_places=2)
    partner_contribution_local = models.DecimalField(max_digits=20, decimal_places=2)
    unicef_cash_local = models.DecimalField(max_digits=20, decimal_places=2)
    in_kind_amount_local = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, blank=True, null=True)
    total_local = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'partners_interventionbudget'
        unique_together = (('id'), ('intervention'),)


class PartnersInterventionplannedvisits(models.Model):
    year = models.IntegerField()
    programmatic_q4 = models.IntegerField()
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    programmatic_q1 = models.IntegerField()
    programmatic_q2 = models.IntegerField()
    programmatic_q3 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'partners_interventionplannedvisits'
        unique_together = (('year', 'intervention'), ('id'),)


class PartnersInterventionreportingperiod(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    due_date = models.DateField()
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'partners_interventionreportingperiod'
        unique_together = (('id'),)


class PartnersInterventionresultlink(models.Model):
    cp_output = models.ForeignKey('ReportsResult', models.DO_NOTHING)
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_interventionresultlink'
        unique_together = (('id'),)


class PartnersInterventionresultlinkRamIndicators(models.Model):
    interventionresultlink = models.ForeignKey(PartnersInterventionresultlink, models.DO_NOTHING)
    indicator = models.ForeignKey('ReportsIndicator', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'partners_interventionresultlink_ram_indicators'
        unique_together = (('id'), ('indicator', 'interventionresultlink'),)


class PartnersInterventionsectorlocationlink(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)
    sector = models.ForeignKey('ReportsSector', models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_interventionsectorlocationlink'
        unique_together = (('id'),)


class PartnersInterventionsectorlocationlinkLocations(models.Model):
    interventionsectorlocationlink = models.ForeignKey(PartnersInterventionsectorlocationlink, models.DO_NOTHING)
    location = models.ForeignKey(LocationsLocation, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'partners_interventionsectorlocationlink_locations'
        unique_together = (('id'), ('interventionsectorlocationlink', 'location'),)


class PartnersPartnerorganization(models.Model):
    partner_type = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    address = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=64, blank=True, null=True)
    vendor_number = models.CharField(max_length=30, blank=True, null=True)
    alternate_id = models.IntegerField(blank=True, null=True)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=50, blank=True, null=True)
    core_values_assessment_date = models.DateField(blank=True, null=True)
    core_values_assessment = models.CharField(max_length=1024, blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = 'partners_partnerorganization'
        unique_together = (('name', 'vendor_number'), ('vendor_number'), ('id'),)


class PartnersPartnerstaffmember(models.Model):
    title = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=128)
    phone = models.CharField(max_length=64, blank=True, null=True)
    partner = models.ForeignKey(PartnersPartnerorganization, models.DO_NOTHING)
    active = models.BooleanField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_partnerstaffmember'
        unique_together = (('email'), ('id'),)


class PartnersPlannedengagement(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    spot_check_mr = models.CharField(max_length=2, blank=True, null=True)
    spot_check_follow_up_q1 = models.IntegerField()
    spot_check_follow_up_q2 = models.IntegerField()
    spot_check_follow_up_q3 = models.IntegerField()
    spot_check_follow_up_q4 = models.IntegerField()
    scheduled_audit = models.BooleanField()
    special_audit = models.BooleanField()
    partner = models.ForeignKey(PartnersPartnerorganization, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'partners_plannedengagement'
        unique_together = (('id'), ('partner'),)


class PartnersWorkspacefiletype(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'partners_workspacefiletype'
        unique_together = (('name'), ('id'),)


class ReportsAppliedindicator(models.Model):
    context_code = models.CharField(max_length=50, blank=True, null=True)
    target = models.IntegerField()
    baseline = models.IntegerField(blank=True, null=True)
    assumptions = models.TextField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    indicator = models.ForeignKey('ReportsIndicatorblueprint', models.DO_NOTHING, blank=True, null=True)
    lower_result = models.ForeignKey('ReportsLowerresult', models.DO_NOTHING)
    means_of_verification = models.CharField(max_length=255, blank=True, null=True)
    cluster_indicator_id = models.IntegerField(blank=True, null=True)
    cluster_indicator_title = models.CharField(max_length=1024, blank=True, null=True)
    cluster_name = models.CharField(max_length=512, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    response_plan_name = models.CharField(max_length=1024, blank=True, null=True)
    section = models.ForeignKey('ReportsSector', models.DO_NOTHING, blank=True, null=True)
    is_active = models.BooleanField()
    is_high_frequency = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'reports_appliedindicator'
        unique_together = (('id'), ('indicator', 'lower_result'),)


class ReportsAppliedindicatorDisaggregation(models.Model):
    appliedindicator = models.ForeignKey(ReportsAppliedindicator, models.DO_NOTHING)
    disaggregation = models.ForeignKey('ReportsDisaggregation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reports_appliedindicator_disaggregation'
        unique_together = (('id'), ('appliedindicator', 'disaggregation'),)


class ReportsAppliedindicatorLocations(models.Model):
    appliedindicator = models.ForeignKey(ReportsAppliedindicator, models.DO_NOTHING)
    location = models.ForeignKey(LocationsLocation, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reports_appliedindicator_locations'
        unique_together = (('id'), ('appliedindicator', 'location'),)


class ReportsCountryprogramme(models.Model):
    name = models.CharField(max_length=150)
    wbs = models.CharField(max_length=30)
    from_date = models.DateField()
    to_date = models.DateField()
    invalid = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'reports_countryprogramme'
        unique_together = (('wbs'), ('id'),)


class ReportsDisaggregation(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=255)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'reports_disaggregation'
        unique_together = (('name'), ('id'),)


class ReportsDisaggregationvalue(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    value = models.CharField(max_length=15)
    active = models.BooleanField()
    disaggregation = models.ForeignKey(ReportsDisaggregation, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reports_disaggregationvalue'
        unique_together = (('id'),)


class ReportsIndicator(models.Model):
    name = models.CharField(max_length=1024)
    code = models.CharField(max_length=50, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    sector_total = models.IntegerField(blank=True, null=True)
    current = models.IntegerField(blank=True, null=True)
    sector_current = models.IntegerField(blank=True, null=True)
    view_on_dashboard = models.BooleanField()
    result = models.ForeignKey('ReportsResult', models.DO_NOTHING, blank=True, null=True)
    sector = models.ForeignKey('ReportsSector', models.DO_NOTHING, blank=True, null=True)
    unit = models.ForeignKey('ReportsUnit', models.DO_NOTHING, blank=True, null=True)
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
        unique_together = (('id'), ('name', 'result', 'sector'),)


class ReportsIndicatorblueprint(models.Model):
    title = models.CharField(max_length=1024)
    description = models.CharField(max_length=3072, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
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
        unique_together = (('id'), ('code'),)


class ReportsLowerresult(models.Model):
    name = models.CharField(max_length=500)
    code = models.CharField(max_length=50)
    result_link = models.ForeignKey(PartnersInterventionresultlink, models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_lowerresult'
        unique_together = (('id'), ('code', 'result_link'),)


class ReportsQuarter(models.Model):
    name = models.CharField(max_length=64)
    year = models.CharField(max_length=4)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_quarter'
        unique_together = (('id'),)


class ReportsReportingrequirement(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    due_date = models.DateField()
    report_type = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reports_reportingrequirement'
        unique_together = (('id'),)


class ReportsResult(models.Model):
    name = models.TextField()
    code = models.CharField(max_length=50, blank=True, null=True)
    result_type = models.ForeignKey('ReportsResulttype', models.DO_NOTHING)
    sector = models.ForeignKey('ReportsSector', models.DO_NOTHING, blank=True, null=True)
    gic_code = models.CharField(max_length=8, blank=True, null=True)
    gic_name = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_tag = models.BooleanField()
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
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
    country_programme = models.ForeignKey(ReportsCountryprogramme, models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_result'
        unique_together = (('wbs', 'country_programme'), ('id'),)


class ReportsResulttype(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'reports_resulttype'
        unique_together = (('name'), ('id'),)


class ReportsSector(models.Model):
    name = models.CharField(max_length=45)
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
        unique_together = (('name'), ('id'),)


class ReportsUnit(models.Model):
    type = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'reports_unit'
        unique_together = (('id'), ('type'),)


class ReversionRevision(models.Model):
    manager_slug = models.CharField(max_length=191)
    date_created = models.DateTimeField()
    comment = models.TextField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reversion_revision'


class ReversionVersion(models.Model):
    object_id = models.TextField()
    object_id_int = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=255)
    serialized_data = models.TextField()
    object_repr = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    revision = models.ForeignKey(ReversionRevision, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reversion_version'


class SnapshotActivity(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    target_object_id = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
    data = models.TextField()  # This field type is a guess.
    change = models.TextField()  # This field type is a guess.
    by_user = models.ForeignKey('AuthUser', models.DO_NOTHING)
    target_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'snapshot_activity'
        unique_together = (('id'),)


class T2FActionpoint(models.Model):
    action_point_number = models.CharField(max_length=11)
    description = models.CharField(max_length=254)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=254)
    completed_at = models.DateTimeField(blank=True, null=True)
    actions_taken = models.TextField()
    follow_up = models.BooleanField()
    comments = models.TextField()
    created_at = models.DateTimeField()
    assigned_by = models.ForeignKey('AuthUser', models.DO_NOTHING)
    person_responsible = models.ForeignKey('AuthUser', models.DO_NOTHING)
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 't2f_actionpoint'
        unique_together = (('id'), ('action_point_number'),)


class T2FClearances(models.Model):
    medical_clearance = models.CharField(max_length=14)
    security_clearance = models.CharField(max_length=14)
    security_course = models.CharField(max_length=14)
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 't2f_clearances'
        unique_together = (('travel'), ('id'),)


class T2FCostassignment(models.Model):
    share = models.IntegerField()
    delegate = models.BooleanField()
    business_area = models.ForeignKey('PublicsBusinessarea', models.DO_NOTHING, blank=True, null=True)
    fund = models.ForeignKey('PublicsFund', models.DO_NOTHING, blank=True, null=True)
    grant = models.ForeignKey('PublicsGrant', models.DO_NOTHING, blank=True, null=True)
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING)
    wbs = models.ForeignKey('PublicsWbs', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_costassignment'
        unique_together = (('id'),)


class T2FDeduction(models.Model):
    date = models.DateField()
    breakfast = models.BooleanField()
    lunch = models.BooleanField()
    dinner = models.BooleanField()
    accomodation = models.BooleanField()
    no_dsa = models.BooleanField()
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 't2f_deduction'
        unique_together = (('id'),)


class T2FExpense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, blank=True, null=True)
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING)
    type = models.ForeignKey('PublicsTravelexpensetype', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_expense'
        unique_together = (('id'),)


class T2FInvoice(models.Model):
    reference_number = models.CharField(max_length=32)
    business_area = models.CharField(max_length=32)
    vendor_number = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    status = models.CharField(max_length=16)
    vision_fi_id = models.CharField(max_length=16)
    currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING)
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING)
    messages = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 't2f_invoice'
        unique_together = (('id'), ('reference_number'),)


class T2FInvoiceitem(models.Model):
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    fund = models.ForeignKey('PublicsFund', models.DO_NOTHING, blank=True, null=True)
    grant = models.ForeignKey('PublicsGrant', models.DO_NOTHING, blank=True, null=True)
    invoice = models.ForeignKey(T2FInvoice, models.DO_NOTHING)
    wbs = models.ForeignKey('PublicsWbs', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_invoiceitem'
        unique_together = (('id'),)


class T2FItineraryitem(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    overnight_travel = models.BooleanField()
    mode_of_travel = models.CharField(max_length=5)
    dsa_region = models.ForeignKey('PublicsDsaregion', models.DO_NOTHING, blank=True, null=True)
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING)
    field_order = models.IntegerField(db_column='_order')  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 't2f_itineraryitem'
        unique_together = (('id'),)


class T2FItineraryitemAirlines(models.Model):
    itineraryitem = models.ForeignKey(T2FItineraryitem, models.DO_NOTHING)
    airlinecompany = models.ForeignKey('PublicsAirlinecompany', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 't2f_itineraryitem_airlines'
        unique_together = (('id'), ('airlinecompany', 'itineraryitem'),)


class T2FTravel(models.Model):
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
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    purpose = models.CharField(max_length=500)
    additional_note = models.TextField()
    international_travel = models.NullBooleanField()
    ta_required = models.NullBooleanField()
    reference_number = models.CharField(max_length=12)
    hidden = models.BooleanField()
    mode_of_travel = models.TextField(blank=True, null=True)  # This field type is a guess.
    estimated_travel_cost = models.DecimalField(max_digits=20, decimal_places=4)
    is_driver = models.BooleanField()
    preserved_expenses_local = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    approved_cost_traveler = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    approved_cost_travel_agencies = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, blank=True, null=True)
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING, blank=True, null=True)
    section = models.ForeignKey('UsersSection', models.DO_NOTHING, blank=True, null=True)
    supervisor = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    traveler = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    first_submission_date = models.DateTimeField(blank=True, null=True)
    preserved_expenses_usd = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    sector = models.ForeignKey(ReportsSector, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_travel'
        unique_together = (('id'), ('reference_number'),)


class T2FTravelactivity(models.Model):
    travel_type = models.CharField(max_length=64)
    date = models.DateTimeField(blank=True, null=True)
    partner = models.ForeignKey(PartnersPartnerorganization, models.DO_NOTHING, blank=True, null=True)
    partnership = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, blank=True, null=True)
    primary_traveler = models.ForeignKey('AuthUser', models.DO_NOTHING)
    result = models.ForeignKey(ReportsResult, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_travelactivity'
        unique_together = (('id'),)


class T2FTravelactivityLocations(models.Model):
    travelactivity = models.ForeignKey(T2FTravelactivity, models.DO_NOTHING)
    location = models.ForeignKey(LocationsLocation, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 't2f_travelactivity_locations'
        unique_together = (('id'), ('travelactivity', 'location'),)


class T2FTravelactivityTravels(models.Model):
    travelactivity = models.ForeignKey(T2FTravelactivity, models.DO_NOTHING)
    travel = models.ForeignKey(T2FTravel, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 't2f_travelactivity_travels'
        unique_together = (('id'), ('travel', 'travelactivity'),)


class T2FTravelattachment(models.Model):
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    file = models.CharField(max_length=255)
    travel = models.ForeignKey(T2FTravel, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 't2f_travelattachment'
        unique_together = (('id'),)


class TpmTpmactionpoint(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    due_date = models.DateField()
    description = models.TextField()
    comments = models.TextField()
    status = models.CharField(max_length=9)
    author = models.ForeignKey('AuthUser', models.DO_NOTHING)
    person_responsible = models.ForeignKey('AuthUser', models.DO_NOTHING)
    tpm_visit = models.ForeignKey('TpmTpmvisit', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tpm_tpmactionpoint'
        unique_together = (('id'),)


class TpmTpmactivity(models.Model):
    activity_ptr = models.ForeignKey(ActivitiesActivity, models.DO_NOTHING, primary_key=True)
    additional_information = models.TextField()
    is_pv = models.BooleanField()
    tpm_visit = models.ForeignKey('TpmTpmvisit', models.DO_NOTHING)
    section = models.ForeignKey(ReportsSector, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tpm_tpmactivity'
        unique_together = (('activity_ptr'),)


class TpmTpmactivityOffices(models.Model):
    tpmactivity = models.ForeignKey(TpmTpmactivity, models.DO_NOTHING)
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tpm_tpmactivity_offices'
        unique_together = (('tpmactivity', 'office'), ('id'),)


class TpmTpmactivityUnicefFocalPoints(models.Model):
    tpmactivity = models.ForeignKey(TpmTpmactivity, models.DO_NOTHING)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tpm_tpmactivity_unicef_focal_points'
        unique_together = (('id'), ('tpmactivity', 'user'),)


class TpmTpmpermission(models.Model):
    user_type = models.CharField(max_length=30)
    permission = models.CharField(max_length=10)
    permission_type = models.CharField(max_length=10)
    target = models.CharField(max_length=100)
    instance_status = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'tpm_tpmpermission'
        unique_together = (('id'), ('target', 'permission_type', 'instance_status', 'user_type'),)


class TpmTpmvisit(models.Model):
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
    tpm_partner = models.ForeignKey('TpmpartnersTpmpartner', models.DO_NOTHING, blank=True, null=True)
    cancel_comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'tpm_tpmvisit'
        unique_together = (('id'),)


class TpmTpmvisitTpmPartnerFocalPoints(models.Model):
    tpmvisit = models.ForeignKey(TpmTpmvisit, models.DO_NOTHING)
    tpmpartnerstaffmember = models.ForeignKey('TpmpartnersTpmpartnerstaffmember', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tpm_tpmvisit_tpm_partner_focal_points'
        unique_together = (('id'), ('tpmvisit', 'tpmpartnerstaffmember'),)


class TpmTpmvisitreportrejectcomment(models.Model):
    rejected_at = models.DateTimeField()
    reject_reason = models.TextField()
    tpm_visit = models.ForeignKey(TpmTpmvisit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tpm_tpmvisitreportrejectcomment'
        unique_together = (('id'),)
