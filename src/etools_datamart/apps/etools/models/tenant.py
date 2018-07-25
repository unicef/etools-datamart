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
    assigned_by = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')
    assigned_to = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')
    author = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')
    cp_output = models.ForeignKey('ReportsResult', models.DO_NOTHING, related_name='+', blank=True, null=True)
    engagement = models.ForeignKey('AuditEngagement', models.DO_NOTHING, related_name='+', blank=True, null=True)
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, related_name='+', blank=True, null=True)
    location = models.ForeignKey('LocationsLocation', models.DO_NOTHING, related_name='+', blank=True, null=True)
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='+')
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='+', blank=True, null=True)
    section = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='+')
    tpm_activity = models.ForeignKey('TpmTpmactivity', models.DO_NOTHING, related_name='+', blank=True, null=True)
    travel_activity = models.ForeignKey('T2FTravelactivity', models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action_points_actionpoint'


class ActivitiesActivity(models.Model):
    date = models.DateField(blank=True, null=True)
    cp_output = models.ForeignKey('ReportsResult', models.DO_NOTHING, related_name='+', blank=True, null=True)
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, related_name='+', blank=True, null=True)
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activities_activity'


class ActivitiesActivityLocations(models.Model):
    activity = models.ForeignKey(ActivitiesActivity, models.DO_NOTHING, related_name='+')
    location = models.ForeignKey('LocationsLocation', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'activities_activity_locations'
        unique_together = (('activity', 'location'),)


class ActstreamAction(models.Model):
    actor_object_id = models.CharField(max_length=255)
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    public = models.BooleanField()
    data = models.TextField(blank=True, null=True)
    action_object_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='+', blank=True, null=True)
    actor_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='+')
    target_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actstream_action'


class ActstreamFollow(models.Model):
    object_id = models.CharField(max_length=255)
    actor_only = models.BooleanField()
    started = models.DateTimeField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='+')
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'actstream_follow'
        unique_together = (('user', 'object_id', 'content_type'),)


class AttachmentsAttachment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    file = models.CharField(max_length=1024, blank=True, null=True)
    hyperlink = models.CharField(max_length=255)
    object_id = models.IntegerField()
    code = models.CharField(max_length=64)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='+')
    file_type = models.ForeignKey('AttachmentsFiletype', models.DO_NOTHING, related_name='+')
    uploaded_by = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attachments_attachment'


class AttachmentsAttachmentflat(models.Model):
    partner = models.CharField(max_length=255)
    partner_type = models.CharField(max_length=150)
    vendor_number = models.CharField(max_length=50)
    pd_ssfa_number = models.CharField(max_length=64)
    file_type = models.CharField(max_length=100)
    file_link = models.CharField(max_length=1024)
    uploaded_by = models.CharField(max_length=255)
    created = models.CharField(max_length=50)
    attachment = models.ForeignKey(AttachmentsAttachment, models.DO_NOTHING, related_name='+')
    filename = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'attachments_attachmentflat'


class AttachmentsFiletype(models.Model):
    order = models.IntegerField()
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    label = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'attachments_filetype'
        unique_together = (('code', 'name'),)


class AuditAudit(models.Model):
    engagement_ptr = models.OneToOneField('AuditEngagement', models.DO_NOTHING, related_name='+')
    audited_expenditure = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    financial_findings = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    audit_opinion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'audit_audit'


class AuditDetailedfindinginfo(models.Model):
    finding = models.TextField()
    recommendation = models.TextField()
    micro_assesment = models.ForeignKey('AuditMicroassessment', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_detailedfindinginfo'


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
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='+')
    joint_audit = models.BooleanField()
    agreement = models.ForeignKey('PurchaseOrderPurchaseorder', models.DO_NOTHING, related_name='+')
    po_item = models.ForeignKey('PurchaseOrderPurchaseorderitem', models.DO_NOTHING, related_name='+', blank=True, null=True)
    shared_ip_with = models.TextField()  # This field type is a guess.
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_engagement'


class AuditEngagementActivePd(models.Model):
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING, related_name='+')
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_engagement_active_pd'
        unique_together = (('intervention', 'engagement'),)


class AuditEngagementAuthorizedOfficers(models.Model):
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING, related_name='+')
    partnerstaffmember = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_engagement_authorized_officers'
        unique_together = (('partnerstaffmember', 'engagement'),)


class AuditEngagementStaffMembers(models.Model):
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING, related_name='+')
    auditorstaffmember = models.ForeignKey('PurchaseOrderAuditorstaffmember', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_engagement_staff_members'
        unique_together = (('auditorstaffmember', 'engagement'),)


class AuditEngagementactionpoint(models.Model):
    category = models.CharField(max_length=100)
    due_date = models.DateField()
    description = models.TextField()
    author = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING, related_name='+')
    person_responsible = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')
    action_taken = models.TextField()
    status = models.CharField(max_length=10)
    high_priority = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'audit_engagementactionpoint'


class AuditFinancialfinding(models.Model):
    title = models.CharField(max_length=255)
    local_amount = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    recommendation = models.TextField()
    ip_comments = models.TextField()
    audit = models.ForeignKey(AuditAudit, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_financialfinding'


class AuditFinding(models.Model):
    priority = models.CharField(max_length=4)
    category_of_observation = models.CharField(max_length=100)
    recommendation = models.TextField()
    agreed_action_by_ip = models.TextField()
    deadline_of_action = models.DateField(blank=True, null=True)
    spot_check = models.ForeignKey('AuditSpotcheck', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_finding'


class AuditKeyinternalcontrol(models.Model):
    recommendation = models.TextField()
    audit_observation = models.TextField()
    ip_response = models.TextField()
    audit = models.ForeignKey(AuditAudit, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_keyinternalcontrol'


class AuditMicroassessment(models.Model):
    engagement_ptr = models.OneToOneField(AuditEngagement, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_microassessment'


class AuditRisk(models.Model):
    value = models.SmallIntegerField(blank=True, null=True)
    extra = models.TextField(blank=True, null=True)  # This field type is a guess.
    blueprint = models.ForeignKey('AuditRiskblueprint', models.DO_NOTHING, related_name='+')
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_risk'
        unique_together = (('blueprint', 'engagement'),)


class AuditRiskblueprint(models.Model):
    order = models.IntegerField()
    weight = models.SmallIntegerField()
    is_key = models.BooleanField()
    header = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('AuditRiskcategory', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_riskblueprint'


class AuditRiskcategory(models.Model):
    order = models.IntegerField()
    header = models.CharField(max_length=255)
    category_type = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    parent = models.ForeignKey('self', models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_riskcategory'


class AuditSpecialaudit(models.Model):
    engagement_ptr = models.OneToOneField(AuditEngagement, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_specialaudit'


class AuditSpecialauditrecommendation(models.Model):
    description = models.TextField()
    audit = models.ForeignKey(AuditSpecialaudit, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_specialauditrecommendation'


class AuditSpecificprocedure(models.Model):
    description = models.TextField()
    finding = models.TextField()
    audit = models.ForeignKey(AuditSpecialaudit, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'audit_specificprocedure'


class AuditSpotcheck(models.Model):
    engagement_ptr = models.OneToOneField(AuditEngagement, models.DO_NOTHING, related_name='+')
    total_amount_tested = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_amount_of_ineligible_expenditure = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    internal_controls = models.TextField()

    class Meta:
        managed = False
        db_table = 'audit_spotcheck'


class DjangoCommentFlags(models.Model):
    flag = models.CharField(max_length=30)
    flag_date = models.DateTimeField()
    comment = models.ForeignKey('DjangoComments', models.DO_NOTHING, related_name='+')
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'django_comment_flags'
        unique_together = (('user', 'comment', 'flag'),)


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
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='+')
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING, related_name='+')
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_comments'


class FundsDonor(models.Model):
    name = models.CharField(max_length=45)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_donor'


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
    fund_commitment = models.ForeignKey(FundsFundscommitmentheader, models.DO_NOTHING, related_name='+')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_fundscommitmentitem'
        unique_together = (('line_item', 'fund_commitment'),)


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
    intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, related_name='+', blank=True, null=True)
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
        unique_together = (('vendor_code', 'fr_number'),)


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
    fund_reservation = models.ForeignKey(FundsFundsreservationheader, models.DO_NOTHING, related_name='+')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_fundsreservationitem'
        unique_together = (('line_item', 'fund_reservation'),)


class FundsGrant(models.Model):
    name = models.CharField(max_length=128)
    donor = models.ForeignKey(FundsDonor, models.DO_NOTHING, related_name='+')
    expiry = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=255)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'funds_grant'


class HactAggregatehact(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.IntegerField()
    partner_values = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'hact_aggregatehact'


class HactHacthistory(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.IntegerField()
    partner_values = models.TextField(blank=True, null=True)  # This field type is a guess.
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'hact_hacthistory'
        unique_together = (('year', 'partner'),)


class LocationsCartodbtable(models.Model):
    domain = models.CharField(max_length=254)
    api_key = models.CharField(max_length=254)
    table_name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254)
    name_col = models.CharField(max_length=254)
    pcode_col = models.CharField(max_length=254)
    parent_code_col = models.CharField(max_length=254)
    color = models.CharField(max_length=7)
    location_type = models.ForeignKey('LocationsGatewaytype', models.DO_NOTHING, related_name='+')
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, related_name='+', blank=True, null=True)
    rght = models.IntegerField()
    tree_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'locations_cartodbtable'


class LocationsGatewaytype(models.Model):
    name = models.CharField(max_length=64)
    admin_level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locations_gatewaytype'


class LocationsLocation(models.Model):
    name = models.CharField(max_length=254)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    p_code = models.CharField(max_length=32)
    point = models.TextField(blank=True, null=True)  # This field type is a guess.
    gateway = models.ForeignKey(LocationsGatewaytype, models.DO_NOTHING, related_name='+')
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, related_name='+', blank=True, null=True)
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'locations_location'
        unique_together = (('gateway', 'p_code', 'name'),)


class ManagementFlaggedissue(models.Model):
    object_id = models.IntegerField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    issue_category = models.CharField(max_length=32)
    issue_id = models.CharField(max_length=100)
    message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='+')
    issue_status = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'management_flaggedissue'


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
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='+')
    partner_manager = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, related_name='+', blank=True, null=True)
    signed_by = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+', blank=True, null=True)
    status = models.CharField(max_length=32)
    country_programme = models.ForeignKey('ReportsCountryprogramme', models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partners_agreement'


class PartnersAgreementAuthorizedOfficers(models.Model):
    agreement = models.ForeignKey(PartnersAgreement, models.DO_NOTHING, related_name='+')
    partnerstaffmember = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'partners_agreement_authorized_officers'
        unique_together = (('partnerstaffmember', 'agreement'),)


class PartnersAgreementamendment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    number = models.CharField(max_length=5)
    signed_amendment = models.CharField(max_length=1024, blank=True, null=True)
    signed_date = models.DateField(blank=True, null=True)
    agreement = models.ForeignKey(PartnersAgreement, models.DO_NOTHING, related_name='+')
    types = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'partners_agreementamendment'


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
    approving_officer = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+', blank=True, null=True)
    partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='+')
    requesting_officer = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+', blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_assessment'


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


class PartnersFiletype(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'partners_filetype'


class PartnersFundingcommitment(models.Model):
    fr_number = models.CharField(max_length=50)
    wbs = models.CharField(max_length=50)
    fc_type = models.CharField(max_length=50)
    fc_ref = models.CharField(max_length=50, blank=True, null=True)
    fr_item_amount_usd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    agreement_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    commitment_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    expenditure_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    grant = models.ForeignKey(FundsGrant, models.DO_NOTHING, related_name='+', blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partners_fundingcommitment'


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
    agreement = models.ForeignKey(PartnersAgreement, models.DO_NOTHING, related_name='+')
    partner_authorized_officer_signatory = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, related_name='+', blank=True, null=True)
    unicef_signatory = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+', blank=True, null=True)
    signed_pd_document = models.CharField(max_length=1024, blank=True, null=True)
    country_programme = models.ForeignKey('ReportsCountryprogramme', models.DO_NOTHING, related_name='+', blank=True, null=True)
    contingency_pd = models.BooleanField()
    metadata = models.TextField(blank=True, null=True)  # This field type is a guess.
    in_amendment = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'partners_intervention'


class PartnersInterventionFlatLocations(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')
    location = models.ForeignKey(LocationsLocation, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'partners_intervention_flat_locations'
        unique_together = (('location', 'intervention'),)


class PartnersInterventionOffices(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'partners_intervention_offices'
        unique_together = (('office', 'intervention'),)


class PartnersInterventionPartnerFocalPoints(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')
    partnerstaffmember = models.ForeignKey('PartnersPartnerstaffmember', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'partners_intervention_partner_focal_points'
        unique_together = (('partnerstaffmember', 'intervention'),)


class PartnersInterventionSections(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')
    sector = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'partners_intervention_sections'
        unique_together = (('sector', 'intervention'),)


class PartnersInterventionUnicefFocalPoints(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'partners_intervention_unicef_focal_points'
        unique_together = (('user', 'intervention'),)


class PartnersInterventionamendment(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    signed_date = models.DateField(blank=True, null=True)
    amendment_number = models.IntegerField()
    signed_amendment = models.CharField(max_length=1024)
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')
    types = models.TextField()  # This field type is a guess.
    other_description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partners_interventionamendment'


class PartnersInterventionattachment(models.Model):
    attachment = models.CharField(max_length=1024)
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')
    type = models.ForeignKey(PartnersFiletype, models.DO_NOTHING, related_name='+')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_interventionattachment'


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
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+', blank=True, null=True)
    total_local = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'partners_interventionbudget'


class PartnersInterventionplannedvisits(models.Model):
    year = models.IntegerField()
    programmatic_q4 = models.IntegerField()
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')
    created = models.DateTimeField()
    modified = models.DateTimeField()
    programmatic_q1 = models.IntegerField()
    programmatic_q2 = models.IntegerField()
    programmatic_q3 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'partners_interventionplannedvisits'
        unique_together = (('year', 'intervention'),)


class PartnersInterventionreportingperiod(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    due_date = models.DateField()
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'partners_interventionreportingperiod'


class PartnersInterventionresultlink(models.Model):
    cp_output = models.ForeignKey('ReportsResult', models.DO_NOTHING, related_name='+')
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_interventionresultlink'


class PartnersInterventionresultlinkRamIndicators(models.Model):
    interventionresultlink = models.ForeignKey(PartnersInterventionresultlink, models.DO_NOTHING, related_name='+')
    indicator = models.ForeignKey('ReportsIndicator', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'partners_interventionresultlink_ram_indicators'
        unique_together = (('interventionresultlink', 'indicator'),)


class PartnersInterventionsectorlocationlink(models.Model):
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')
    sector = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='+')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_interventionsectorlocationlink'


class PartnersInterventionsectorlocationlinkLocations(models.Model):
    interventionsectorlocationlink = models.ForeignKey(PartnersInterventionsectorlocationlink, models.DO_NOTHING, related_name='+')
    location = models.ForeignKey(LocationsLocation, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'partners_interventionsectorlocationlink_locations'
        unique_together = (('location', 'interventionsectorlocationlink'),)


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
        unique_together = (('vendor_number', 'name'),)


class PartnersPartnerstaffmember(models.Model):
    title = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=128)
    phone = models.CharField(max_length=64, blank=True, null=True)
    partner = models.ForeignKey(PartnersPartnerorganization, models.DO_NOTHING, related_name='+')
    active = models.BooleanField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partners_partnerstaffmember'


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
    partner = models.ForeignKey(PartnersPartnerorganization, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'partners_plannedengagement'


class PartnersWorkspacefiletype(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'partners_workspacefiletype'


class ReportsAppliedindicator(models.Model):
    context_code = models.CharField(max_length=50, blank=True, null=True)
    target = models.IntegerField()
    baseline = models.IntegerField(blank=True, null=True)
    assumptions = models.TextField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    indicator = models.ForeignKey('ReportsIndicatorblueprint', models.DO_NOTHING, related_name='+', blank=True, null=True)
    lower_result = models.ForeignKey('ReportsLowerresult', models.DO_NOTHING, related_name='+')
    means_of_verification = models.CharField(max_length=255, blank=True, null=True)
    cluster_indicator_id = models.IntegerField(blank=True, null=True)
    cluster_indicator_title = models.CharField(max_length=1024, blank=True, null=True)
    cluster_name = models.CharField(max_length=512, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    response_plan_name = models.CharField(max_length=1024, blank=True, null=True)
    section = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='+', blank=True, null=True)
    is_active = models.BooleanField()
    is_high_frequency = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'reports_appliedindicator'
        unique_together = (('indicator', 'lower_result'),)


class ReportsAppliedindicatorDisaggregation(models.Model):
    appliedindicator = models.ForeignKey(ReportsAppliedindicator, models.DO_NOTHING, related_name='+')
    disaggregation = models.ForeignKey('ReportsDisaggregation', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'reports_appliedindicator_disaggregation'
        unique_together = (('appliedindicator', 'disaggregation'),)


class ReportsAppliedindicatorLocations(models.Model):
    appliedindicator = models.ForeignKey(ReportsAppliedindicator, models.DO_NOTHING, related_name='+')
    location = models.ForeignKey(LocationsLocation, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'reports_appliedindicator_locations'
        unique_together = (('location', 'appliedindicator'),)


class ReportsCountryprogramme(models.Model):
    name = models.CharField(max_length=150)
    wbs = models.CharField(max_length=30)
    from_date = models.DateField()
    to_date = models.DateField()
    invalid = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'reports_countryprogramme'


class ReportsDisaggregation(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=255)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'reports_disaggregation'


class ReportsDisaggregationvalue(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    value = models.CharField(max_length=15)
    active = models.BooleanField()
    disaggregation = models.ForeignKey(ReportsDisaggregation, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'reports_disaggregationvalue'


class ReportsIndicator(models.Model):
    name = models.CharField(max_length=1024)
    code = models.CharField(max_length=50, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    sector_total = models.IntegerField(blank=True, null=True)
    current = models.IntegerField(blank=True, null=True)
    sector_current = models.IntegerField(blank=True, null=True)
    view_on_dashboard = models.BooleanField()
    result = models.ForeignKey('ReportsResult', models.DO_NOTHING, related_name='+', blank=True, null=True)
    sector = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='+', blank=True, null=True)
    unit = models.ForeignKey('ReportsUnit', models.DO_NOTHING, related_name='+', blank=True, null=True)
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
        unique_together = (('sector', 'result', 'name'),)


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


class ReportsLowerresult(models.Model):
    name = models.CharField(max_length=500)
    code = models.CharField(max_length=50)
    result_link = models.ForeignKey(PartnersInterventionresultlink, models.DO_NOTHING, related_name='+')
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_lowerresult'
        unique_together = (('code', 'result_link'),)


class ReportsQuarter(models.Model):
    name = models.CharField(max_length=64)
    year = models.CharField(max_length=4)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_quarter'


class ReportsReportingrequirement(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    due_date = models.DateField()
    report_type = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    intervention = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'reports_reportingrequirement'


class ReportsResult(models.Model):
    name = models.TextField()
    code = models.CharField(max_length=50, blank=True, null=True)
    result_type = models.ForeignKey('ReportsResulttype', models.DO_NOTHING, related_name='+')
    sector = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='+', blank=True, null=True)
    gic_code = models.CharField(max_length=8, blank=True, null=True)
    gic_name = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_tag = models.BooleanField()
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, related_name='+', blank=True, null=True)
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
    country_programme = models.ForeignKey(ReportsCountryprogramme, models.DO_NOTHING, related_name='+', blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports_result'
        unique_together = (('country_programme', 'wbs'),)


class ReportsResulttype(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'reports_resulttype'


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


class ReportsUnit(models.Model):
    type = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'reports_unit'


class SnapshotActivity(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    target_object_id = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
    data = models.TextField()  # This field type is a guess.
    change = models.TextField()  # This field type is a guess.
    by_user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')
    target_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'snapshot_activity'


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
    assigned_by = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')
    person_responsible = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 't2f_actionpoint'


class T2FClearances(models.Model):
    medical_clearance = models.CharField(max_length=14)
    security_clearance = models.CharField(max_length=14)
    security_course = models.CharField(max_length=14)
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 't2f_clearances'


class T2FCostassignment(models.Model):
    share = models.IntegerField()
    delegate = models.BooleanField()
    business_area = models.ForeignKey('PublicsBusinessarea', models.DO_NOTHING, related_name='+', blank=True, null=True)
    fund = models.ForeignKey('PublicsFund', models.DO_NOTHING, related_name='+', blank=True, null=True)
    grant = models.ForeignKey('PublicsGrant', models.DO_NOTHING, related_name='+', blank=True, null=True)
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING, related_name='+')
    wbs = models.ForeignKey('PublicsWbs', models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_costassignment'


class T2FDeduction(models.Model):
    date = models.DateField()
    breakfast = models.BooleanField()
    lunch = models.BooleanField()
    dinner = models.BooleanField()
    accomodation = models.BooleanField()
    no_dsa = models.BooleanField()
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 't2f_deduction'


class T2FExpense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, related_name='+', blank=True, null=True)
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING, related_name='+')
    type = models.ForeignKey('PublicsTravelexpensetype', models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_expense'


class T2FInvoice(models.Model):
    reference_number = models.CharField(max_length=32)
    business_area = models.CharField(max_length=32)
    vendor_number = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    status = models.CharField(max_length=16)
    vision_fi_id = models.CharField(max_length=16)
    currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, related_name='+')
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING, related_name='+')
    messages = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 't2f_invoice'


class T2FInvoiceitem(models.Model):
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    fund = models.ForeignKey('PublicsFund', models.DO_NOTHING, related_name='+', blank=True, null=True)
    grant = models.ForeignKey('PublicsGrant', models.DO_NOTHING, related_name='+', blank=True, null=True)
    invoice = models.ForeignKey(T2FInvoice, models.DO_NOTHING, related_name='+')
    wbs = models.ForeignKey('PublicsWbs', models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_invoiceitem'


class T2FItineraryitem(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    overnight_travel = models.BooleanField()
    mode_of_travel = models.CharField(max_length=5)
    dsa_region = models.ForeignKey('PublicsDsaregion', models.DO_NOTHING, related_name='+', blank=True, null=True)
    travel = models.ForeignKey('T2FTravel', models.DO_NOTHING, related_name='+')
    field_order = models.IntegerField(db_column='_order')  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 't2f_itineraryitem'


class T2FItineraryitemAirlines(models.Model):
    itineraryitem = models.ForeignKey(T2FItineraryitem, models.DO_NOTHING, related_name='+')
    airlinecompany = models.ForeignKey('PublicsAirlinecompany', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 't2f_itineraryitem_airlines'
        unique_together = (('airlinecompany', 'itineraryitem'),)


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
    currency = models.ForeignKey('PublicsCurrency', models.DO_NOTHING, related_name='+', blank=True, null=True)
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='+', blank=True, null=True)
    section = models.ForeignKey('UsersSection', models.DO_NOTHING, related_name='+', blank=True, null=True)
    supervisor = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+', blank=True, null=True)
    traveler = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+', blank=True, null=True)
    first_submission_date = models.DateTimeField(blank=True, null=True)
    preserved_expenses_usd = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    sector = models.ForeignKey(ReportsSector, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_travel'


class T2FTravelactivity(models.Model):
    travel_type = models.CharField(max_length=64)
    date = models.DateTimeField(blank=True, null=True)
    partner = models.ForeignKey(PartnersPartnerorganization, models.DO_NOTHING, related_name='+', blank=True, null=True)
    partnership = models.ForeignKey(PartnersIntervention, models.DO_NOTHING, related_name='+', blank=True, null=True)
    primary_traveler = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')
    result = models.ForeignKey(ReportsResult, models.DO_NOTHING, related_name='+', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't2f_travelactivity'


class T2FTravelactivityLocations(models.Model):
    travelactivity = models.ForeignKey(T2FTravelactivity, models.DO_NOTHING, related_name='+')
    location = models.ForeignKey(LocationsLocation, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 't2f_travelactivity_locations'
        unique_together = (('location', 'travelactivity'),)


class T2FTravelactivityTravels(models.Model):
    travelactivity = models.ForeignKey(T2FTravelactivity, models.DO_NOTHING, related_name='+')
    travel = models.ForeignKey(T2FTravel, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 't2f_travelactivity_travels'
        unique_together = (('travelactivity', 'travel'),)


class T2FTravelattachment(models.Model):
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    file = models.CharField(max_length=255)
    travel = models.ForeignKey(T2FTravel, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 't2f_travelattachment'


class TpmTpmactionpoint(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    due_date = models.DateField()
    description = models.TextField()
    comments = models.TextField()
    status = models.CharField(max_length=9)
    author = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')
    person_responsible = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')
    tpm_visit = models.ForeignKey('TpmTpmvisit', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'tpm_tpmactionpoint'


class TpmTpmactivity(models.Model):
    activity_ptr = models.OneToOneField(ActivitiesActivity, models.DO_NOTHING, related_name='+')
    additional_information = models.TextField()
    is_pv = models.BooleanField()
    tpm_visit = models.ForeignKey('TpmTpmvisit', models.DO_NOTHING, related_name='+')
    section = models.ForeignKey(ReportsSector, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'tpm_tpmactivity'


class TpmTpmactivityOffices(models.Model):
    tpmactivity = models.ForeignKey(TpmTpmactivity, models.DO_NOTHING, related_name='+')
    office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'tpm_tpmactivity_offices'
        unique_together = (('tpmactivity', 'office'),)


class TpmTpmactivityUnicefFocalPoints(models.Model):
    tpmactivity = models.ForeignKey(TpmTpmactivity, models.DO_NOTHING, related_name='+')
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'tpm_tpmactivity_unicef_focal_points'
        unique_together = (('tpmactivity', 'user'),)


class TpmTpmpermission(models.Model):
    user_type = models.CharField(max_length=30)
    permission = models.CharField(max_length=10)
    permission_type = models.CharField(max_length=10)
    target = models.CharField(max_length=100)
    instance_status = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'tpm_tpmpermission'
        unique_together = (('target', 'user_type', 'instance_status', 'permission_type'),)


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
    tpm_partner = models.ForeignKey('TpmpartnersTpmpartner', models.DO_NOTHING, related_name='+', blank=True, null=True)
    cancel_comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'tpm_tpmvisit'


class TpmTpmvisitTpmPartnerFocalPoints(models.Model):
    tpmvisit = models.ForeignKey(TpmTpmvisit, models.DO_NOTHING, related_name='+')
    tpmpartnerstaffmember = models.ForeignKey('TpmpartnersTpmpartnerstaffmember', models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'tpm_tpmvisit_tpm_partner_focal_points'
        unique_together = (('tpmvisit', 'tpmpartnerstaffmember'),)


class TpmTpmvisitreportrejectcomment(models.Model):
    rejected_at = models.DateTimeField()
    reject_reason = models.TextField()
    tpm_visit = models.ForeignKey(TpmTpmvisit, models.DO_NOTHING, related_name='+')

    class Meta:
        managed = False
        db_table = 'tpm_tpmvisitreportrejectcomment'
