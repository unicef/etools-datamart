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
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=10)
    description = models.TextField()
    due_date = models.DateField(blank=True, null=True)
    date_of_completion = models.DateTimeField(blank=True, null=True)
    assigned_by = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="ActionPointsActionpoint_assigned_by")
    assigned_to = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="ActionPointsActionpoint_assigned_to")
    author = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="ActionPointsActionpoint_author")
    cp_output = models.ForeignKey(
        "ReportsResult", models.DO_NOTHING, related_name="ActionPointsActionpoint_cp_output", blank=True, null=True
    )
    engagement = models.ForeignKey(
        "AuditEngagement", models.DO_NOTHING, related_name="ActionPointsActionpoint_engagement", blank=True, null=True
    )
    intervention = models.ForeignKey(
        "PartnersIntervention",
        models.DO_NOTHING,
        related_name="ActionPointsActionpoint_intervention",
        blank=True,
        null=True,
    )
    location = models.ForeignKey(
        "LocationsLocation", models.DO_NOTHING, related_name="ActionPointsActionpoint_location", blank=True, null=True
    )
    office = models.ForeignKey(
        "ReportsOffice", models.DO_NOTHING, related_name="ActionPointsActionpoint_office", blank=True, null=True
    )
    partner = models.ForeignKey(
        "PartnersPartnerorganization",
        models.DO_NOTHING,
        related_name="ActionPointsActionpoint_partner",
        blank=True,
        null=True,
    )
    section = models.ForeignKey(
        "ReportsSector", models.DO_NOTHING, related_name="ActionPointsActionpoint_section", blank=True, null=True
    )
    tpm_activity = models.ForeignKey(
        "TpmTpmactivity", models.DO_NOTHING, related_name="ActionPointsActionpoint_tpm_activity", blank=True, null=True
    )
    high_priority = models.BooleanField()
    travel_activity = models.ForeignKey(
        "T2FTravelactivity",
        models.DO_NOTHING,
        related_name="ActionPointsActionpoint_travel_activity",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        "CategoriesCategory", models.DO_NOTHING, related_name="ActionPointsActionpoint_category", blank=True, null=True
    )
    psea_assessment = models.ForeignKey(
        "PseaAssessment",
        models.DO_NOTHING,
        related_name="ActionPointsActionpoint_psea_assessment",
        blank=True,
        null=True,
    )
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    monitoring_activity = models.ForeignKey(
        "FieldMonitoringPlanningMonitoringactivity",
        models.DO_NOTHING,
        related_name="ActionPointsActionpoint_monitoring_activity",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "action_points_actionpoint"


class ActivitiesActivity(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    cp_output = models.ForeignKey(
        "ReportsResult", models.DO_NOTHING, related_name="ActivitiesActivity_cp_output", blank=True, null=True
    )
    intervention = models.ForeignKey(
        "PartnersIntervention", models.DO_NOTHING, related_name="ActivitiesActivity_intervention", blank=True, null=True
    )
    partner = models.ForeignKey(
        "PartnersPartnerorganization",
        models.DO_NOTHING,
        related_name="ActivitiesActivity_partner",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "activities_activity"


class ActivitiesActivityLocations(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    activity = models.ForeignKey(
        ActivitiesActivity, models.DO_NOTHING, related_name="ActivitiesActivityLocations_activity"
    )
    location = models.ForeignKey(
        "LocationsLocation", models.DO_NOTHING, related_name="ActivitiesActivityLocations_location"
    )

    class Meta:
        managed = False
        db_table = "activities_activity_locations"
        unique_together = (("activity", "location"),)


class ActstreamAction(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    actor_object_id = models.CharField(max_length=255)
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    public = models.BooleanField()
    data = models.TextField(blank=True, null=True)
    action_object_content_type = models.ForeignKey(
        "DjangoContentType",
        models.DO_NOTHING,
        related_name="ActstreamAction_action_object_content_type",
        blank=True,
        null=True,
    )
    actor_content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, related_name="ActstreamAction_actor_content_type"
    )
    target_content_type = models.ForeignKey(
        "DjangoContentType",
        models.DO_NOTHING,
        related_name="ActstreamAction_target_content_type",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "actstream_action"


class ActstreamFollow(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    object_id = models.CharField(max_length=255)
    actor_only = models.BooleanField()
    started = models.DateTimeField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, related_name="ActstreamFollow_content_type"
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="ActstreamFollow_user")

    class Meta:
        managed = False
        db_table = "actstream_follow"
        unique_together = (("content_type", "object_id", "user"),)


class AttachmentsAttachmentflat(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    partner = models.CharField(max_length=255)
    partner_type = models.CharField(max_length=150)
    vendor_number = models.CharField(max_length=50)
    pd_ssfa_number = models.CharField(max_length=64)
    file_type = models.CharField(max_length=100)
    file_link = models.CharField(max_length=1024)
    uploaded_by = models.CharField(max_length=255)
    attachment = models.ForeignKey(
        "UnicefAttachmentsAttachment", models.DO_NOTHING, related_name="AttachmentsAttachmentflat_attachment"
    )
    filename = models.CharField(max_length=1024)
    agreement_reference_number = models.CharField(max_length=100)
    object_link = models.CharField(max_length=200)
    source = models.CharField(max_length=150)
    pd_ssfa = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField()

    class Meta:
        managed = False
        db_table = "attachments_attachmentflat"


class AuditAudit(models.TenantModel):
    engagement_ptr = models.OneToOneField(
        "AuditEngagement", models.DO_NOTHING, related_name="AuditAudit_engagement_ptr"
    )
    audited_expenditure = models.DecimalField(max_digits=20, decimal_places=2)
    financial_findings = models.DecimalField(max_digits=20, decimal_places=2)
    audit_opinion = models.CharField(max_length=20)
    audited_expenditure_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    financial_findings_local = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "audit_audit"


class AuditDetailedfindinginfo(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    finding = models.TextField()
    recommendation = models.TextField()
    micro_assesment = models.ForeignKey(
        "AuditMicroassessment", models.DO_NOTHING, related_name="AuditDetailedfindinginfo_micro_assesment"
    )

    class Meta:
        managed = False
        db_table = "audit_detailedfindinginfo"


class AuditEngagement(models.TenantModel):
    id = models.IntegerField(primary_key=True)
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
    partner = models.ForeignKey(
        "PartnersPartnerorganization", models.DO_NOTHING, related_name="AuditEngagement_partner"
    )
    joint_audit = models.BooleanField()
    agreement = models.ForeignKey(
        "PurchaseOrderPurchaseorder", models.DO_NOTHING, related_name="AuditEngagement_agreement"
    )
    po_item = models.ForeignKey(
        "PurchaseOrderPurchaseorderitem",
        models.DO_NOTHING,
        related_name="AuditEngagement_po_item",
        blank=True,
        null=True,
    )
    shared_ip_with = models.TextField()  # This field type is a guess.
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=2)
    currency_of_report = models.CharField(max_length=5, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    year_of_audit = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "audit_engagement"


class AuditEngagementActivePd(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    engagement = models.ForeignKey(
        AuditEngagement, models.DO_NOTHING, related_name="AuditEngagementActivePd_engagement"
    )
    intervention = models.ForeignKey(
        "PartnersIntervention", models.DO_NOTHING, related_name="AuditEngagementActivePd_intervention"
    )

    class Meta:
        managed = False
        db_table = "audit_engagement_active_pd"
        unique_together = (("engagement", "intervention"),)


class AuditEngagementAuthorizedOfficers(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    engagement = models.ForeignKey(
        AuditEngagement, models.DO_NOTHING, related_name="AuditEngagementAuthorizedOfficers_engagement"
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="AuditEngagementAuthorizedOfficers_user")

    class Meta:
        managed = False
        db_table = "audit_engagement_authorized_officers"
        unique_together = (("engagement", "user"),)


class AuditEngagementOffices(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING, related_name="AuditEngagementOffices_engagement")
    office = models.ForeignKey("ReportsOffice", models.DO_NOTHING, related_name="AuditEngagementOffices_office")

    class Meta:
        managed = False
        db_table = "audit_engagement_offices"
        unique_together = (("engagement", "office"),)


class AuditEngagementSections(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    engagement = models.ForeignKey(
        AuditEngagement, models.DO_NOTHING, related_name="AuditEngagementSections_engagement"
    )
    section = models.ForeignKey("ReportsSector", models.DO_NOTHING, related_name="AuditEngagementSections_section")

    class Meta:
        managed = False
        db_table = "audit_engagement_sections"
        unique_together = (("engagement", "section"),)


class AuditEngagementStaffMembers(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    engagement = models.ForeignKey(
        AuditEngagement, models.DO_NOTHING, related_name="AuditEngagementStaffMembers_engagement"
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="AuditEngagementStaffMembers_user")

    class Meta:
        managed = False
        db_table = "audit_engagement_staff_members"
        unique_together = (("engagement", "user"),)


class AuditEngagementUsersNotified(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    engagement = models.ForeignKey(
        AuditEngagement, models.DO_NOTHING, related_name="AuditEngagementUsersNotified_engagement"
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="AuditEngagementUsersNotified_user")

    class Meta:
        managed = False
        db_table = "audit_engagement_users_notified"
        unique_together = (("engagement", "user"),)


class AuditFinancialfinding(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    local_amount = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    recommendation = models.TextField()
    ip_comments = models.TextField()
    audit = models.ForeignKey(AuditAudit, models.DO_NOTHING, related_name="AuditFinancialfinding_audit")

    class Meta:
        managed = False
        db_table = "audit_financialfinding"


class AuditFinding(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    priority = models.CharField(max_length=4)
    category_of_observation = models.CharField(max_length=100)
    recommendation = models.TextField()
    agreed_action_by_ip = models.TextField()
    deadline_of_action = models.DateField(blank=True, null=True)
    spot_check = models.ForeignKey("AuditSpotcheck", models.DO_NOTHING, related_name="AuditFinding_spot_check")

    class Meta:
        managed = False
        db_table = "audit_finding"


class AuditKeyinternalcontrol(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    recommendation = models.TextField()
    audit_observation = models.TextField()
    ip_response = models.TextField()
    audit = models.ForeignKey(AuditAudit, models.DO_NOTHING, related_name="AuditKeyinternalcontrol_audit")

    class Meta:
        managed = False
        db_table = "audit_keyinternalcontrol"


class AuditMicroassessment(models.TenantModel):
    engagement_ptr = models.OneToOneField(
        AuditEngagement, models.DO_NOTHING, related_name="AuditMicroassessment_engagement_ptr"
    )
    questionnaire_version = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = "audit_microassessment"


class AuditRisk(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    value = models.SmallIntegerField(blank=True, null=True)
    extra = models.JSONField(blank=True, null=True)
    blueprint = models.ForeignKey("AuditRiskblueprint", models.DO_NOTHING, related_name="AuditRisk_blueprint")
    engagement = models.ForeignKey(AuditEngagement, models.DO_NOTHING, related_name="AuditRisk_engagement")

    class Meta:
        managed = False
        db_table = "audit_risk"


class AuditRiskblueprint(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    order = models.IntegerField()
    weight = models.SmallIntegerField()
    is_key = models.BooleanField()
    header = models.TextField()
    description = models.TextField()
    category = models.ForeignKey("AuditRiskcategory", models.DO_NOTHING, related_name="AuditRiskblueprint_category")

    class Meta:
        managed = False
        db_table = "audit_riskblueprint"


class AuditRiskcategory(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    order = models.IntegerField()
    header = models.CharField(max_length=500)
    category_type = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    parent = models.ForeignKey(
        "self", models.DO_NOTHING, related_name="AuditRiskcategory_parent", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "audit_riskcategory"


class AuditSpecialaudit(models.TenantModel):
    engagement_ptr = models.OneToOneField(
        AuditEngagement, models.DO_NOTHING, related_name="AuditSpecialaudit_engagement_ptr"
    )

    class Meta:
        managed = False
        db_table = "audit_specialaudit"


class AuditSpecialauditrecommendation(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    audit = models.ForeignKey(
        AuditSpecialaudit, models.DO_NOTHING, related_name="AuditSpecialauditrecommendation_audit"
    )

    class Meta:
        managed = False
        db_table = "audit_specialauditrecommendation"


class AuditSpecificprocedure(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    finding = models.TextField()
    audit = models.ForeignKey(AuditSpecialaudit, models.DO_NOTHING, related_name="AuditSpecificprocedure_audit")

    class Meta:
        managed = False
        db_table = "audit_specificprocedure"


class AuditSpotcheck(models.TenantModel):
    engagement_ptr = models.OneToOneField(
        AuditEngagement, models.DO_NOTHING, related_name="AuditSpotcheck_engagement_ptr"
    )
    total_amount_tested = models.DecimalField(max_digits=20, decimal_places=2)
    total_amount_of_ineligible_expenditure = models.DecimalField(max_digits=20, decimal_places=2)
    internal_controls = models.TextField()

    class Meta:
        managed = False
        db_table = "audit_spotcheck"


class CommentsComment(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    state = models.CharField(max_length=10)
    instance_related_id = models.IntegerField()
    related_to_description = models.TextField()
    related_to = models.CharField(max_length=100)
    text = models.TextField()
    instance_related_ct = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, related_name="CommentsComment_instance_related_ct"
    )
    parent = models.ForeignKey("self", models.DO_NOTHING, related_name="CommentsComment_parent", blank=True, null=True)
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="CommentsComment_user")

    class Meta:
        managed = False
        db_table = "comments_comment"


class CommentsCommentUsersRelated(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    comment = models.ForeignKey(CommentsComment, models.DO_NOTHING, related_name="CommentsCommentUsersRelated_comment")
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="CommentsCommentUsersRelated_user")

    class Meta:
        managed = False
        db_table = "comments_comment_users_related"
        unique_together = (("comment", "user"),)


class DjangoCommentFlags(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    flag = models.CharField(max_length=30)
    flag_date = models.DateTimeField()
    comment = models.ForeignKey("DjangoComments", models.DO_NOTHING, related_name="DjangoCommentFlags_comment")
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="DjangoCommentFlags_user")

    class Meta:
        managed = False
        db_table = "django_comment_flags"
        unique_together = (("comment", "flag", "user"),)


class DjangoComments(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    object_pk = models.CharField(max_length=64)
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=254)
    user_url = models.CharField(max_length=200)
    comment = models.TextField()
    submit_date = models.DateTimeField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    is_public = models.BooleanField()
    is_removed = models.BooleanField()
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING, related_name="DjangoComments_content_type")
    site = models.ForeignKey("DjangoSite", models.DO_NOTHING, related_name="DjangoComments_site")
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="DjangoComments_user", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "django_comments"


class FieldMonitoringDataCollectionActivityoverallfinding(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    narrative_finding = models.TextField()
    on_track = models.BooleanField(blank=True, null=True)
    cp_output = models.ForeignKey(
        "ReportsResult",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionActivityoverallfinding_cp_output",
        blank=True,
        null=True,
    )
    intervention = models.ForeignKey(
        "PartnersIntervention",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionActivityoverallfinding_intervention",
        blank=True,
        null=True,
    )
    monitoring_activity = models.ForeignKey(
        "FieldMonitoringPlanningMonitoringactivity",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionActivityoverallfinding_monitoring_activity",
    )
    partner = models.ForeignKey(
        "PartnersPartnerorganization",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionActivityoverallfinding_partner",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_data_collection_activityoverallfinding"


class FieldMonitoringDataCollectionActivityquestion(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    specific_details = models.TextField()
    is_enabled = models.BooleanField()
    cp_output = models.ForeignKey(
        "ReportsResult",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionActivityquestion_cp_output",
        blank=True,
        null=True,
    )
    intervention = models.ForeignKey(
        "PartnersIntervention",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionActivityquestion_intervention",
        blank=True,
        null=True,
    )
    monitoring_activity = models.ForeignKey(
        "FieldMonitoringPlanningMonitoringactivity",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionActivityquestion_monitoring_activity",
    )
    partner = models.ForeignKey(
        "PartnersPartnerorganization",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionActivityquestion_partner",
        blank=True,
        null=True,
    )
    question = models.ForeignKey(
        "FieldMonitoringSettingsQuestion",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionActivityquestion_question",
    )
    is_hact = models.BooleanField()
    text = models.TextField()

    class Meta:
        managed = False
        db_table = "field_monitoring_data_collection_activityquestion"


class FieldMonitoringDataCollectionActivityquestionoverallfinding(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    value = models.JSONField(blank=True, null=True)
    activity_question = models.OneToOneField(
        FieldMonitoringDataCollectionActivityquestion,
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionActivityquestionoverallfinding_activity_question",
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_data_collection_activityquestionoverallfinding"


class FieldMonitoringDataCollectionChecklistoverallfinding(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    narrative_finding = models.TextField()
    cp_output = models.ForeignKey(
        "ReportsResult",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionChecklistoverallfinding_cp_output",
        blank=True,
        null=True,
    )
    intervention = models.ForeignKey(
        "PartnersIntervention",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionChecklistoverallfinding_intervention",
        blank=True,
        null=True,
    )
    partner = models.ForeignKey(
        "PartnersPartnerorganization",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionChecklistoverallfinding_partner",
        blank=True,
        null=True,
    )
    started_checklist = models.ForeignKey(
        "FieldMonitoringDataCollectionStartedchecklist",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionChecklistoverallfinding_started_checklist",
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_data_collection_checklistoverallfinding"


class FieldMonitoringDataCollectionFinding(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    value = models.JSONField(blank=True, null=True)
    activity_question = models.ForeignKey(
        FieldMonitoringDataCollectionActivityquestion,
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionFinding_activity_question",
    )
    started_checklist = models.ForeignKey(
        "FieldMonitoringDataCollectionStartedchecklist",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionFinding_started_checklist",
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_data_collection_finding"


class FieldMonitoringDataCollectionStartedchecklist(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    information_source = models.CharField(max_length=100)
    author = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="FieldMonitoringDataCollectionStartedchecklist_author"
    )
    method = models.ForeignKey(
        "FieldMonitoringSettingsMethod",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionStartedchecklist_method",
    )
    monitoring_activity = models.ForeignKey(
        "FieldMonitoringPlanningMonitoringactivity",
        models.DO_NOTHING,
        related_name="FieldMonitoringDataCollectionStartedchecklist_monitoring_activity",
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_data_collection_startedchecklist"


class FieldMonitoringPlanningMonitoringactivity(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    deleted_at = models.DateTimeField()
    monitor_type = models.CharField(max_length=10)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20)
    location = models.ForeignKey(
        "LocationsLocation",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivity_location",
        blank=True,
        null=True,
    )
    location_site = models.ForeignKey(
        "FieldMonitoringSettingsLocationsite",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivity_location_site",
        blank=True,
        null=True,
    )
    visit_lead = models.ForeignKey(
        "AuthUser",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivity_visit_lead",
        blank=True,
        null=True,
    )
    tpm_partner = models.ForeignKey(
        "TpmpartnersTpmpartner",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivity_tpm_partner",
        blank=True,
        null=True,
    )
    cancel_reason = models.TextField()
    reject_reason = models.TextField()
    field_office = models.ForeignKey(
        "ReportsOffice",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivity_field_office",
        blank=True,
        null=True,
    )
    report_reject_reason = models.TextField()
    number = models.CharField(unique=True, max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "field_monitoring_planning_monitoringactivity"


class FieldMonitoringPlanningMonitoringactivityCpOutputs(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    monitoringactivity = models.ForeignKey(
        FieldMonitoringPlanningMonitoringactivity,
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivityCpOutputs_monitoringactivity",
    )
    result = models.ForeignKey(
        "ReportsResult", models.DO_NOTHING, related_name="FieldMonitoringPlanningMonitoringactivityCpOutputs_result"
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_planning_monitoringactivity_cp_outputs"
        unique_together = (("monitoringactivity", "result"),)


class FieldMonitoringPlanningMonitoringactivityInterventions(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    monitoringactivity = models.ForeignKey(
        FieldMonitoringPlanningMonitoringactivity,
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivityInterventions_monitoringactivity",
    )
    intervention = models.ForeignKey(
        "PartnersIntervention",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivityInterventions_intervention",
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_planning_monitoringactivity_interventions"
        unique_together = (("intervention", "monitoringactivity"),)


class FieldMonitoringPlanningMonitoringactivityOffices(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    monitoringactivity = models.ForeignKey(
        FieldMonitoringPlanningMonitoringactivity,
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivityOffices_monitoringactivity",
    )
    office = models.ForeignKey(
        "ReportsOffice", models.DO_NOTHING, related_name="FieldMonitoringPlanningMonitoringactivityOffices_office"
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_planning_monitoringactivity_offices"
        unique_together = (("monitoringactivity", "office"),)


class FieldMonitoringPlanningMonitoringactivityPartners(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    monitoringactivity = models.ForeignKey(
        FieldMonitoringPlanningMonitoringactivity,
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivityPartners_monitoringactivity",
    )
    partnerorganization = models.ForeignKey(
        "PartnersPartnerorganization",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivityPartners_partnerorganization",
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_planning_monitoringactivity_partners"
        unique_together = (("monitoringactivity", "partnerorganization"),)


class FieldMonitoringPlanningMonitoringactivitySections(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    monitoringactivity = models.ForeignKey(
        FieldMonitoringPlanningMonitoringactivity,
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivitySections_monitoringactivity",
    )
    section = models.ForeignKey(
        "ReportsSector", models.DO_NOTHING, related_name="FieldMonitoringPlanningMonitoringactivitySections_section"
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_planning_monitoringactivity_sections"
        unique_together = (("monitoringactivity", "section"),)


class FieldMonitoringPlanningMonitoringactivityTeamMembers(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    monitoringactivity = models.ForeignKey(
        FieldMonitoringPlanningMonitoringactivity,
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivityTeamMembers_monitoringactivity",
    )
    user = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="FieldMonitoringPlanningMonitoringactivityTeamMembers_user"
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_planning_monitoringactivity_team_members"
        unique_together = (("monitoringactivity", "user"),)


class FieldMonitoringPlanningMonitoringactivitygroup(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    partner = models.ForeignKey(
        "PartnersPartnerorganization",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivitygroup_partner",
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_planning_monitoringactivitygroup"


class FieldMonitoringPlanningMonitoringactivitygroupMonitorin69Fc(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    monitoringactivitygroup = models.ForeignKey(
        FieldMonitoringPlanningMonitoringactivitygroup,
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivitygroupMonitorin69Fc_monitoringactivitygroup",
    )
    monitoringactivity = models.ForeignKey(
        FieldMonitoringPlanningMonitoringactivity,
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningMonitoringactivitygroupMonitorin69Fc_monitoringactivity",
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_planning_monitoringactivitygroup_monitorin69fc"
        unique_together = (("monitoringactivity", "monitoringactivitygroup"),)


class FieldMonitoringPlanningQuestiontemplate(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    is_active = models.BooleanField()
    specific_details = models.TextField()
    cp_output = models.ForeignKey(
        "ReportsResult",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningQuestiontemplate_cp_output",
        blank=True,
        null=True,
    )
    intervention = models.ForeignKey(
        "PartnersIntervention",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningQuestiontemplate_intervention",
        blank=True,
        null=True,
    )
    partner = models.ForeignKey(
        "PartnersPartnerorganization",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningQuestiontemplate_partner",
        blank=True,
        null=True,
    )
    question = models.ForeignKey(
        "FieldMonitoringSettingsQuestion",
        models.DO_NOTHING,
        related_name="FieldMonitoringPlanningQuestiontemplate_question",
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_planning_questiontemplate"


class FieldMonitoringPlanningYearplan(models.TenantModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.SmallIntegerField(primary_key=True)
    prioritization_criteria = models.TextField()
    methodology_notes = models.TextField()
    target_visits = models.SmallIntegerField()
    modalities = models.TextField()
    partner_engagement = models.TextField()
    other_aspects = models.TextField()

    class Meta:
        managed = False
        db_table = "field_monitoring_planning_yearplan"


class FieldMonitoringSettingsCategory(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    order = models.IntegerField()
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "field_monitoring_settings_category"


class FieldMonitoringSettingsGlobalconfig(models.TenantModel):
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "field_monitoring_settings_globalconfig"


class FieldMonitoringSettingsLocationsite(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=254)
    p_code = models.CharField(max_length=32)
    point = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_active = models.BooleanField()
    parent = models.ForeignKey(
        "LocationsLocation", models.DO_NOTHING, related_name="FieldMonitoringSettingsLocationsite_parent"
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_settings_locationsite"


class FieldMonitoringSettingsLogissue(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    issue = models.TextField()
    status = models.CharField(max_length=10)
    author = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="FieldMonitoringSettingsLogissue_author")
    cp_output = models.ForeignKey(
        "ReportsResult",
        models.DO_NOTHING,
        related_name="FieldMonitoringSettingsLogissue_cp_output",
        blank=True,
        null=True,
    )
    location = models.ForeignKey(
        "LocationsLocation",
        models.DO_NOTHING,
        related_name="FieldMonitoringSettingsLogissue_location",
        blank=True,
        null=True,
    )
    location_site = models.ForeignKey(
        FieldMonitoringSettingsLocationsite,
        models.DO_NOTHING,
        related_name="FieldMonitoringSettingsLogissue_location_site",
        blank=True,
        null=True,
    )
    partner = models.ForeignKey(
        "PartnersPartnerorganization",
        models.DO_NOTHING,
        related_name="FieldMonitoringSettingsLogissue_partner",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_settings_logissue"


class FieldMonitoringSettingsMethod(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    use_information_source = models.BooleanField()
    short_name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "field_monitoring_settings_method"


class FieldMonitoringSettingsOption(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    label = models.CharField(max_length=100)
    value = models.JSONField(blank=True, null=True)
    question = models.ForeignKey(
        "FieldMonitoringSettingsQuestion", models.DO_NOTHING, related_name="FieldMonitoringSettingsOption_question"
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_settings_option"
        unique_together = (("question", "value"),)


class FieldMonitoringSettingsQuestion(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    answer_type = models.CharField(max_length=15)
    choices_size = models.SmallIntegerField(blank=True, null=True)
    level = models.CharField(max_length=15)
    text = models.TextField()
    is_hact = models.BooleanField()
    is_custom = models.BooleanField()
    is_active = models.BooleanField()
    category = models.ForeignKey(
        FieldMonitoringSettingsCategory, models.DO_NOTHING, related_name="FieldMonitoringSettingsQuestion_category"
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_settings_question"


class FieldMonitoringSettingsQuestionMethods(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(
        FieldMonitoringSettingsQuestion,
        models.DO_NOTHING,
        related_name="FieldMonitoringSettingsQuestionMethods_question",
    )
    method = models.ForeignKey(
        FieldMonitoringSettingsMethod, models.DO_NOTHING, related_name="FieldMonitoringSettingsQuestionMethods_method"
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_settings_question_methods"
        unique_together = (("method", "question"),)


class FieldMonitoringSettingsQuestionSections(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(
        FieldMonitoringSettingsQuestion,
        models.DO_NOTHING,
        related_name="FieldMonitoringSettingsQuestionSections_question",
    )
    section = models.ForeignKey(
        "ReportsSector", models.DO_NOTHING, related_name="FieldMonitoringSettingsQuestionSections_section"
    )

    class Meta:
        managed = False
        db_table = "field_monitoring_settings_question_sections"
        unique_together = (("question", "section"),)


class FundsDonor(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=45)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "funds_donor"


class FundsFundscommitmentheader(models.TenantModel):
    id = models.IntegerField(primary_key=True)
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
        db_table = "funds_fundscommitmentheader"


class FundsFundscommitmentitem(models.TenantModel):
    id = models.IntegerField(primary_key=True)
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
    fund_commitment = models.ForeignKey(
        FundsFundscommitmentheader, models.DO_NOTHING, related_name="FundsFundscommitmentitem_fund_commitment"
    )
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "funds_fundscommitmentitem"
        unique_together = (("fund_commitment", "line_item"),)


class FundsFundsreservationheader(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    vendor_code = models.CharField(max_length=20)
    fr_number = models.CharField(unique=True, max_length=20)
    document_date = models.DateField(blank=True, null=True)
    fr_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    document_text = models.CharField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    actual_amt = models.DecimalField(max_digits=20, decimal_places=2)
    intervention = models.ForeignKey(
        "PartnersIntervention",
        models.DO_NOTHING,
        related_name="FundsFundsreservationheader_intervention",
        blank=True,
        null=True,
    )
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
        db_table = "funds_fundsreservationheader"
        unique_together = (("fr_number", "vendor_code"),)


class FundsFundsreservationitem(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    fr_ref_number = models.CharField(max_length=30)
    line_item = models.SmallIntegerField()
    wbs = models.CharField(max_length=30)
    grant_number = models.CharField(max_length=20)
    fund = models.CharField(max_length=10)
    overall_amount = models.DecimalField(max_digits=20, decimal_places=2)
    overall_amount_dc = models.DecimalField(max_digits=20, decimal_places=2)
    due_date = models.DateField(blank=True, null=True)
    line_item_text = models.CharField(max_length=255, blank=True, null=True)
    fund_reservation = models.ForeignKey(
        FundsFundsreservationheader, models.DO_NOTHING, related_name="FundsFundsreservationitem_fund_reservation"
    )
    created = models.DateTimeField()
    modified = models.DateTimeField()
    donor = models.CharField(max_length=256, blank=True, null=True)
    donor_code = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "funds_fundsreservationitem"
        unique_together = (("fund_reservation", "line_item"),)


class FundsGrant(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=128)
    donor = models.ForeignKey(FundsDonor, models.DO_NOTHING, related_name="FundsGrant_donor")
    expiry = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=255)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "funds_grant"


class HactAggregatehact(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.IntegerField(unique=True)
    partner_values = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "hact_aggregatehact"


class HactHacthistory(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.IntegerField()
    partner_values = models.JSONField(blank=True, null=True)
    partner = models.ForeignKey(
        "PartnersPartnerorganization", models.DO_NOTHING, related_name="HactHacthistory_partner"
    )

    class Meta:
        managed = False
        db_table = "hact_hacthistory"
        unique_together = (("partner", "year"),)


class LocationsLocation(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=254)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    p_code = models.CharField(max_length=32)
    point = models.TextField(blank=True, null=True)  # This field type is a guess.
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey(
        "self", models.DO_NOTHING, related_name="LocationsLocation_parent", blank=True, null=True
    )
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    is_active = models.BooleanField()
    admin_level = models.SmallIntegerField(blank=True, null=True)
    admin_level_name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "locations_location"
        unique_together = (("admin_level", "name", "p_code"),)


class ManagementSectionhistory(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    history_type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "management_sectionhistory"


class ManagementSectionhistoryFromSections(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    sectionhistory = models.ForeignKey(
        ManagementSectionhistory, models.DO_NOTHING, related_name="ManagementSectionhistoryFromSections_sectionhistory"
    )
    section = models.ForeignKey(
        "ReportsSector", models.DO_NOTHING, related_name="ManagementSectionhistoryFromSections_section"
    )

    class Meta:
        managed = False
        db_table = "management_sectionhistory_from_sections"
        unique_together = (("section", "sectionhistory"),)


class ManagementSectionhistoryToSections(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    sectionhistory = models.ForeignKey(
        ManagementSectionhistory, models.DO_NOTHING, related_name="ManagementSectionhistoryToSections_sectionhistory"
    )
    section = models.ForeignKey(
        "ReportsSector", models.DO_NOTHING, related_name="ManagementSectionhistoryToSections_section"
    )

    class Meta:
        managed = False
        db_table = "management_sectionhistory_to_sections"
        unique_together = (("section", "sectionhistory"),)


class PartnersAgreement(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    agreement_type = models.CharField(max_length=10)
    agreement_number = models.CharField(unique=True, max_length=45)
    attached_agreement = models.CharField(max_length=1024)
    signed_by_unicef_date = models.DateField(blank=True, null=True)
    signed_by_partner_date = models.DateField(blank=True, null=True)
    partner = models.ForeignKey(
        "PartnersPartnerorganization", models.DO_NOTHING, related_name="PartnersAgreement_partner"
    )
    signed_by = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="PartnersAgreement_signed_by", blank=True, null=True
    )
    status = models.CharField(max_length=32)
    country_programme = models.ForeignKey(
        "ReportsCountryprogramme",
        models.DO_NOTHING,
        related_name="PartnersAgreement_country_programme",
        blank=True,
        null=True,
    )
    reference_number_year = models.IntegerField()
    special_conditions_pca = models.BooleanField()
    terms_acknowledged_by = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="PartnersAgreement_terms_acknowledged_by", blank=True, null=True
    )
    partner_manager = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="PartnersAgreement_partner_manager", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "partners_agreement"


class PartnersAgreementAuthorizedOfficers(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    agreement = models.ForeignKey(
        PartnersAgreement, models.DO_NOTHING, related_name="PartnersAgreementAuthorizedOfficers_agreement"
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="PartnersAgreementAuthorizedOfficers_user")

    class Meta:
        managed = False
        db_table = "partners_agreement_authorized_officers"
        unique_together = (("agreement", "user"),)


class PartnersAgreementamendment(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    number = models.CharField(max_length=5)
    signed_amendment = models.CharField(max_length=1024, blank=True, null=True)
    signed_date = models.DateField(blank=True, null=True)
    agreement = models.ForeignKey(
        PartnersAgreement, models.DO_NOTHING, related_name="PartnersAgreementamendment_agreement"
    )
    types = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "partners_agreementamendment"


class PartnersAssessment(models.TenantModel):
    id = models.IntegerField(primary_key=True)
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
    approving_officer = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="PartnersAssessment_approving_officer", blank=True, null=True
    )
    partner = models.ForeignKey(
        "PartnersPartnerorganization", models.DO_NOTHING, related_name="PartnersAssessment_partner"
    )
    requesting_officer = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="PartnersAssessment_requesting_officer", blank=True, null=True
    )
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "partners_assessment"


class PartnersCorevaluesassessment(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    date = models.DateField(blank=True, null=True)
    assessment = models.CharField(max_length=1024, blank=True, null=True)
    archived = models.BooleanField()
    partner = models.ForeignKey(
        "PartnersPartnerorganization", models.DO_NOTHING, related_name="PartnersCorevaluesassessment_partner"
    )

    class Meta:
        managed = False
        db_table = "partners_corevaluesassessment"


class PartnersDirectcashtransfer(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    fc_ref = models.CharField(max_length=50)
    amount_usd = models.DecimalField(max_digits=20, decimal_places=2)
    liquidation_usd = models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_balance_usd = models.DecimalField(max_digits=20, decimal_places=2)
    amount_less_than_3_months_usd = models.DecimalField(
        db_column="amount_less_than_3_Months_usd", max_digits=20, decimal_places=2
    )  # Field name made lowercase.
    amount_3_to_6_months_usd = models.DecimalField(max_digits=20, decimal_places=2)
    amount_6_to_9_months_usd = models.DecimalField(max_digits=20, decimal_places=2)
    amount_more_than_9_months_usd = models.DecimalField(
        db_column="amount_more_than_9_Months_usd", max_digits=20, decimal_places=2
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "partners_directcashtransfer"


class PartnersFiletype(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        managed = False
        db_table = "partners_filetype"


class PartnersIntervention(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    document_type = models.CharField(max_length=255)
    number = models.CharField(unique=True, max_length=64, blank=True, null=True)
    title = models.CharField(max_length=306)
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
    agreement = models.ForeignKey(PartnersAgreement, models.DO_NOTHING, related_name="PartnersIntervention_agreement")
    unicef_signatory = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="PartnersIntervention_unicef_signatory", blank=True, null=True
    )
    signed_pd_document = models.CharField(max_length=1024, blank=True, null=True)
    country_programme = models.ForeignKey(
        "ReportsCountryprogramme",
        models.DO_NOTHING,
        related_name="PartnersIntervention_country_programme",
        blank=True,
        null=True,
    )
    contingency_pd = models.BooleanField()
    metadata = models.JSONField(blank=True, null=True)
    in_amendment = models.BooleanField()
    reference_number_year = models.IntegerField(blank=True, null=True)
    activation_letter = models.CharField(max_length=1024, blank=True, null=True)
    termination_doc = models.CharField(max_length=1024, blank=True, null=True)
    cfei_number = models.CharField(max_length=150, blank=True, null=True)
    budget_owner = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="PartnersIntervention_budget_owner", blank=True, null=True
    )
    context = models.TextField(blank=True, null=True)
    date_sent_to_partner = models.DateField(blank=True, null=True)
    equity_narrative = models.TextField(blank=True, null=True)
    equity_rating = models.CharField(max_length=50)
    gender_narrative = models.TextField(blank=True, null=True)
    gender_rating = models.CharField(max_length=50)
    hq_support_cost = models.DecimalField(max_digits=2, decimal_places=1)
    implementation_strategy = models.TextField(blank=True, null=True)
    ip_program_contribution = models.TextField(blank=True, null=True)
    partner_accepted = models.BooleanField()
    sustainability_narrative = models.TextField(blank=True, null=True)
    sustainability_rating = models.CharField(max_length=50)
    unicef_accepted = models.BooleanField()
    unicef_court = models.BooleanField()
    unicef_review_type = models.CharField(max_length=50)
    humanitarian_flag = models.BooleanField()
    capacity_development = models.TextField(blank=True, null=True)
    other_info = models.TextField(blank=True, null=True)
    other_partners_involved = models.TextField(blank=True, null=True)
    technical_guidance = models.TextField(blank=True, null=True)
    cash_transfer_modalities = models.TextField()  # This field type is a guess.
    cancel_justification = models.TextField(blank=True, null=True)
    date_partnership_review_performed = models.DateField(blank=True, null=True)
    accepted_on_behalf_of_partner = models.BooleanField()
    activation_protocol = models.TextField(blank=True, null=True)
    confidential = models.BooleanField()
    has_activities_involving_children = models.BooleanField()
    has_data_processing_agreement = models.BooleanField()
    has_special_conditions_for_construction = models.BooleanField()
    final_review_approved = models.BooleanField()
    other_details = models.TextField(blank=True, null=True)
    partner_authorized_officer_signatory = models.ForeignKey(
        "AuthUser",
        models.DO_NOTHING,
        related_name="PartnersIntervention_partner_authorized_officer_signatory",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "partners_intervention"


class PartnersInterventionCountryProgrammes(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionCountryProgrammes_intervention"
    )
    countryprogramme = models.ForeignKey(
        "ReportsCountryprogramme",
        models.DO_NOTHING,
        related_name="PartnersInterventionCountryProgrammes_countryprogramme",
    )

    class Meta:
        managed = False
        db_table = "partners_intervention_country_programmes"
        unique_together = (("countryprogramme", "intervention"),)


class PartnersInterventionFlatLocations(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionFlatLocations_intervention"
    )
    location = models.ForeignKey(
        LocationsLocation, models.DO_NOTHING, related_name="PartnersInterventionFlatLocations_location"
    )

    class Meta:
        managed = False
        db_table = "partners_intervention_flat_locations"
        unique_together = (("intervention", "location"),)


class PartnersInterventionOffices(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionOffices_intervention"
    )
    office = models.ForeignKey("ReportsOffice", models.DO_NOTHING, related_name="PartnersInterventionOffices_office")

    class Meta:
        managed = False
        db_table = "partners_intervention_offices"
        unique_together = (("intervention", "office"),)


class PartnersInterventionPartnerFocalPoints(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionPartnerFocalPoints_intervention"
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="PartnersInterventionPartnerFocalPoints_user")

    class Meta:
        managed = False
        db_table = "partners_intervention_partner_focal_points"
        unique_together = (("intervention", "user"),)


class PartnersInterventionSections(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionSections_intervention"
    )
    section = models.ForeignKey("ReportsSector", models.DO_NOTHING, related_name="PartnersInterventionSections_section")

    class Meta:
        managed = False
        db_table = "partners_intervention_sections"
        unique_together = (("intervention", "section"),)


class PartnersInterventionSites(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionSites_intervention"
    )
    locationsite = models.ForeignKey(
        FieldMonitoringSettingsLocationsite, models.DO_NOTHING, related_name="PartnersInterventionSites_locationsite"
    )

    class Meta:
        managed = False
        db_table = "partners_intervention_sites"
        unique_together = (("intervention", "locationsite"),)


class PartnersInterventionUnicefFocalPoints(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionUnicefFocalPoints_intervention"
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="PartnersInterventionUnicefFocalPoints_user")

    class Meta:
        managed = False
        db_table = "partners_intervention_unicef_focal_points"
        unique_together = (("intervention", "user"),)


class PartnersInterventionamendment(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    signed_date = models.DateField(blank=True, null=True)
    amendment_number = models.CharField(max_length=15)
    signed_amendment = models.CharField(max_length=1024)
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionamendment_intervention"
    )
    types = models.TextField()  # This field type is a guess.
    other_description = models.CharField(max_length=512, blank=True, null=True)
    amended_intervention = models.OneToOneField(
        PartnersIntervention,
        models.DO_NOTHING,
        related_name="PartnersInterventionamendment_amended_intervention",
        blank=True,
        null=True,
    )
    difference = models.JSONField()
    is_active = models.BooleanField()
    kind = models.CharField(max_length=20)
    related_objects_map = models.JSONField()
    signed_by_partner_date = models.DateField(blank=True, null=True)
    signed_by_unicef_date = models.DateField(blank=True, null=True)
    unicef_signatory = models.ForeignKey(
        "AuthUser",
        models.DO_NOTHING,
        related_name="PartnersInterventionamendment_unicef_signatory",
        blank=True,
        null=True,
    )
    partner_authorized_officer_signatory = models.ForeignKey(
        "AuthUser",
        models.DO_NOTHING,
        related_name="PartnersInterventionamendment_partner_authorized_officer_signatory",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "partners_interventionamendment"


class PartnersInterventionattachment(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    attachment = models.CharField(max_length=1024)
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionattachment_intervention"
    )
    type = models.ForeignKey(PartnersFiletype, models.DO_NOTHING, related_name="PartnersInterventionattachment_type")
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "partners_interventionattachment"


class PartnersInterventionbudget(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    partner_contribution = models.DecimalField(max_digits=20, decimal_places=2)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2)
    in_kind_amount = models.DecimalField(max_digits=20, decimal_places=2)
    partner_contribution_local = models.DecimalField(max_digits=20, decimal_places=2)
    unicef_cash_local = models.DecimalField(max_digits=20, decimal_places=2)
    in_kind_amount_local = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    intervention = models.OneToOneField(
        PartnersIntervention,
        models.DO_NOTHING,
        related_name="PartnersInterventionbudget_intervention",
        blank=True,
        null=True,
    )
    total_local = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=5)
    programme_effectiveness = models.DecimalField(max_digits=20, decimal_places=2)
    total_hq_cash_local = models.DecimalField(max_digits=20, decimal_places=2)
    total_unicef_cash_local_wo_hq = models.DecimalField(max_digits=20, decimal_places=2)
    partner_supply_local = models.DecimalField(max_digits=20, decimal_places=2)
    total_partner_contribution_local = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        managed = False
        db_table = "partners_interventionbudget"


class PartnersInterventionmanagementbudget(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    act1_unicef = models.DecimalField(max_digits=20, decimal_places=2)
    act1_partner = models.DecimalField(max_digits=20, decimal_places=2)
    act2_unicef = models.DecimalField(max_digits=20, decimal_places=2)
    act2_partner = models.DecimalField(max_digits=20, decimal_places=2)
    act3_unicef = models.DecimalField(max_digits=20, decimal_places=2)
    act3_partner = models.DecimalField(max_digits=20, decimal_places=2)
    intervention = models.OneToOneField(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionmanagementbudget_intervention"
    )

    class Meta:
        managed = False
        db_table = "partners_interventionmanagementbudget"


class PartnersInterventionmanagementbudgetitem(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=15)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2)
    cso_cash = models.DecimalField(max_digits=20, decimal_places=2)
    budget = models.ForeignKey(
        PartnersInterventionmanagementbudget,
        models.DO_NOTHING,
        related_name="PartnersInterventionmanagementbudgetitem_budget",
    )
    no_units = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.CharField(max_length=150)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        managed = False
        db_table = "partners_interventionmanagementbudgetitem"


class PartnersInterventionplannedvisits(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField()
    programmatic_q4 = models.IntegerField()
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionplannedvisits_intervention"
    )
    created = models.DateTimeField()
    modified = models.DateTimeField()
    programmatic_q1 = models.IntegerField()
    programmatic_q2 = models.IntegerField()
    programmatic_q3 = models.IntegerField()

    class Meta:
        managed = False
        db_table = "partners_interventionplannedvisits"
        unique_together = (("intervention", "year"),)


class PartnersInterventionplannedvisitsite(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    quarter = models.SmallIntegerField()
    planned_visits = models.ForeignKey(
        PartnersInterventionplannedvisits,
        models.DO_NOTHING,
        related_name="PartnersInterventionplannedvisitsite_planned_visits",
    )
    site = models.ForeignKey(
        FieldMonitoringSettingsLocationsite, models.DO_NOTHING, related_name="PartnersInterventionplannedvisitsite_site"
    )

    class Meta:
        managed = False
        db_table = "partners_interventionplannedvisitsite"
        unique_together = (("planned_visits", "quarter", "site"),)


class PartnersInterventionreportingperiod(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    due_date = models.DateField()
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionreportingperiod_intervention"
    )

    class Meta:
        managed = False
        db_table = "partners_interventionreportingperiod"


class PartnersInterventionresultlink(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    cp_output = models.ForeignKey(
        "ReportsResult",
        models.DO_NOTHING,
        related_name="PartnersInterventionresultlink_cp_output",
        blank=True,
        null=True,
    )
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionresultlink_intervention"
    )
    created = models.DateTimeField()
    modified = models.DateTimeField()
    code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "partners_interventionresultlink"
        unique_together = (("cp_output", "intervention"),)


class PartnersInterventionresultlinkRamIndicators(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    interventionresultlink = models.ForeignKey(
        PartnersInterventionresultlink,
        models.DO_NOTHING,
        related_name="PartnersInterventionresultlinkRamIndicators_interventionresultlink",
    )
    indicator = models.ForeignKey(
        "ReportsIndicator", models.DO_NOTHING, related_name="PartnersInterventionresultlinkRamIndicators_indicator"
    )

    class Meta:
        managed = False
        db_table = "partners_interventionresultlink_ram_indicators"
        unique_together = (("indicator", "interventionresultlink"),)


class PartnersInterventionreview(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    review_type = models.CharField(max_length=50)
    overall_approval = models.BooleanField(blank=True, null=True)
    amendment = models.ForeignKey(
        PartnersInterventionamendment,
        models.DO_NOTHING,
        related_name="PartnersInterventionreview_amendment",
        blank=True,
        null=True,
    )
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionreview_intervention"
    )
    actions_list = models.TextField()
    budget_is_aligned = models.CharField(max_length=100)
    ges_considered = models.CharField(max_length=100)
    meeting_date = models.DateField(blank=True, null=True)
    overall_approver = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="PartnersInterventionreview_overall_approver", blank=True, null=True
    )
    overall_comment = models.TextField()
    partner_comparative_advantage = models.CharField(max_length=100)
    pd_is_guided = models.CharField(max_length=100)
    pd_is_relevant = models.CharField(max_length=100)
    relationship_is_represented = models.CharField(max_length=10)
    relationships_are_positive = models.CharField(max_length=100)
    supply_issues_considered = models.CharField(max_length=100)
    submitted_by = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="PartnersInterventionreview_submitted_by", blank=True, null=True
    )
    review_date = models.DateField(blank=True, null=True)
    sent_back_comment = models.TextField()

    class Meta:
        managed = False
        db_table = "partners_interventionreview"


class PartnersInterventionreviewPrcOfficers(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    interventionreview = models.ForeignKey(
        PartnersInterventionreview,
        models.DO_NOTHING,
        related_name="PartnersInterventionreviewPrcOfficers_interventionreview",
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="PartnersInterventionreviewPrcOfficers_user")

    class Meta:
        managed = False
        db_table = "partners_interventionreview_prc_officers"
        unique_together = (("interventionreview", "user"),)


class PartnersInterventionreviewnotification(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    review = models.ForeignKey(
        PartnersInterventionreview, models.DO_NOTHING, related_name="PartnersInterventionreviewnotification_review"
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="PartnersInterventionreviewnotification_user")

    class Meta:
        managed = False
        db_table = "partners_interventionreviewnotification"


class PartnersInterventionrisk(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    risk_type = models.CharField(max_length=50)
    mitigation_measures = models.TextField()
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionrisk_intervention"
    )

    class Meta:
        managed = False
        db_table = "partners_interventionrisk"


class PartnersInterventionsupplyitem(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    title = models.CharField(max_length=150)
    unit_number = models.DecimalField(max_digits=20, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    other_mentions = models.TextField()
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="PartnersInterventionsupplyitem_intervention"
    )
    result = models.ForeignKey(
        PartnersInterventionresultlink,
        models.DO_NOTHING,
        related_name="PartnersInterventionsupplyitem_result",
        blank=True,
        null=True,
    )
    unicef_product_number = models.CharField(max_length=150)
    provided_by = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "partners_interventionsupplyitem"


class PartnersPartnerorganization(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=256)
    address = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=64, blank=True, null=True)
    alternate_id = models.IntegerField(blank=True, null=True)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=50, blank=True, null=True)
    core_values_assessment_date = models.DateField(blank=True, null=True)
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
    hact_values = models.JSONField(blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    net_ct_cy = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    reported_cy = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_ct_ytd = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    basis_for_risk_rating = models.CharField(max_length=50)
    manually_blocked = models.BooleanField()
    outstanding_dct_amount_6_to_9_months_usd = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    outstanding_dct_amount_more_than_9_months_usd = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    highest_risk_rating_name = models.CharField(max_length=150)
    highest_risk_rating_type = models.CharField(max_length=150)
    psea_assessment_date = models.DateTimeField(blank=True, null=True)
    sea_risk_rating_name = models.CharField(max_length=150)
    lead_office = models.ForeignKey(
        "ReportsOffice",
        models.DO_NOTHING,
        related_name="PartnersPartnerorganization_lead_office",
        blank=True,
        null=True,
    )
    lead_section = models.ForeignKey(
        "ReportsSector",
        models.DO_NOTHING,
        related_name="PartnersPartnerorganization_lead_section",
        blank=True,
        null=True,
    )
    organization = models.OneToOneField(
        "OrganizationsOrganization", models.DO_NOTHING, related_name="PartnersPartnerorganization_organization"
    )

    class Meta:
        managed = False
        db_table = "partners_partnerorganization"


class PartnersPartnerplannedvisits(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.IntegerField()
    programmatic_q1 = models.IntegerField()
    programmatic_q2 = models.IntegerField()
    programmatic_q3 = models.IntegerField()
    programmatic_q4 = models.IntegerField()
    partner = models.ForeignKey(
        PartnersPartnerorganization, models.DO_NOTHING, related_name="PartnersPartnerplannedvisits_partner"
    )

    class Meta:
        managed = False
        db_table = "partners_partnerplannedvisits"
        unique_together = (("partner", "year"),)


class PartnersPlannedengagement(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    spot_check_planned_q1 = models.IntegerField()
    spot_check_planned_q2 = models.IntegerField()
    spot_check_planned_q3 = models.IntegerField()
    spot_check_planned_q4 = models.IntegerField()
    scheduled_audit = models.BooleanField()
    special_audit = models.BooleanField()
    partner = models.OneToOneField(
        PartnersPartnerorganization, models.DO_NOTHING, related_name="PartnersPlannedengagement_partner"
    )
    spot_check_follow_up = models.IntegerField()

    class Meta:
        managed = False
        db_table = "partners_plannedengagement"


class PartnersPrcofficerinterventionreview(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    relationship_is_represented = models.CharField(max_length=10)
    partner_comparative_advantage = models.CharField(max_length=100)
    relationships_are_positive = models.CharField(max_length=100)
    pd_is_relevant = models.CharField(max_length=100)
    pd_is_guided = models.CharField(max_length=100)
    ges_considered = models.CharField(max_length=100)
    budget_is_aligned = models.CharField(max_length=100)
    supply_issues_considered = models.CharField(max_length=100)
    overall_comment = models.TextField()
    overall_approval = models.BooleanField(blank=True, null=True)
    overall_review = models.ForeignKey(
        PartnersInterventionreview,
        models.DO_NOTHING,
        related_name="PartnersPrcofficerinterventionreview_overall_review",
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="PartnersPrcofficerinterventionreview_user")
    review_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "partners_prcofficerinterventionreview"


class PartnersWorkspacefiletype(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        managed = False
        db_table = "partners_workspacefiletype"


class PseaAnswer(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    comments = models.TextField(blank=True, null=True)
    assessment = models.ForeignKey("PseaAssessment", models.DO_NOTHING, related_name="PseaAnswer_assessment")
    indicator = models.ForeignKey("PseaIndicator", models.DO_NOTHING, related_name="PseaAnswer_indicator")
    rating = models.ForeignKey("PseaRating", models.DO_NOTHING, related_name="PseaAnswer_rating")

    class Meta:
        managed = False
        db_table = "psea_answer"
        unique_together = (("assessment", "indicator"),)


class PseaAnswerevidence(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    answer = models.ForeignKey(PseaAnswer, models.DO_NOTHING, related_name="PseaAnswerevidence_answer")
    evidence = models.ForeignKey("PseaEvidence", models.DO_NOTHING, related_name="PseaAnswerevidence_evidence")

    class Meta:
        managed = False
        db_table = "psea_answerevidence"


class PseaAssessment(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    reference_number = models.CharField(unique=True, max_length=100)
    overall_rating = models.IntegerField(blank=True, null=True)
    assessment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30)
    partner = models.ForeignKey(PartnersPartnerorganization, models.DO_NOTHING, related_name="PseaAssessment_partner")
    assessment_ingo_reason = models.CharField(max_length=32, blank=True, null=True)
    assessment_type = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = "psea_assessment"


class PseaAssessmentFocalPoints(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    assessment = models.ForeignKey(
        PseaAssessment, models.DO_NOTHING, related_name="PseaAssessmentFocalPoints_assessment"
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="PseaAssessmentFocalPoints_user")

    class Meta:
        managed = False
        db_table = "psea_assessment_focal_points"
        unique_together = (("assessment", "user"),)


class PseaAssessmentstatushistory(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=30)
    assessment = models.ForeignKey(
        PseaAssessment, models.DO_NOTHING, related_name="PseaAssessmentstatushistory_assessment"
    )
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = "psea_assessmentstatushistory"


class PseaAssessor(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    assessor_type = models.CharField(max_length=30)
    order_number = models.CharField(max_length=30)
    assessment = models.OneToOneField(PseaAssessment, models.DO_NOTHING, related_name="PseaAssessor_assessment")
    auditor_firm = models.ForeignKey(
        "PurchaseOrderAuditorfirm", models.DO_NOTHING, related_name="PseaAssessor_auditor_firm", blank=True, null=True
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="PseaAssessor_user", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "psea_assessor"


class PseaAssessorAuditorFirmStaff(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    assessor = models.ForeignKey(PseaAssessor, models.DO_NOTHING, related_name="PseaAssessorAuditorFirmStaff_assessor")
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="PseaAssessorAuditorFirmStaff_user")

    class Meta:
        managed = False
        db_table = "psea_assessor_auditor_firm_staff"
        unique_together = (("assessor", "user"),)


class PseaEvidence(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    label = models.TextField()
    requires_description = models.BooleanField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "psea_evidence"


class PseaIndicator(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    subject = models.TextField()
    content = models.TextField()
    active = models.BooleanField()
    order = models.IntegerField()
    rating_instructions = models.TextField()

    class Meta:
        managed = False
        db_table = "psea_indicator"


class PseaIndicatorEvidences(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    indicator = models.ForeignKey(PseaIndicator, models.DO_NOTHING, related_name="PseaIndicatorEvidences_indicator")
    evidence = models.ForeignKey(PseaEvidence, models.DO_NOTHING, related_name="PseaIndicatorEvidences_evidence")

    class Meta:
        managed = False
        db_table = "psea_indicator_evidences"
        unique_together = (("evidence", "indicator"),)


class PseaIndicatorRatings(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    indicator = models.ForeignKey(PseaIndicator, models.DO_NOTHING, related_name="PseaIndicatorRatings_indicator")
    rating = models.ForeignKey("PseaRating", models.DO_NOTHING, related_name="PseaIndicatorRatings_rating")

    class Meta:
        managed = False
        db_table = "psea_indicator_ratings"
        unique_together = (("indicator", "rating"),)


class PseaRating(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    label = models.CharField(max_length=50)
    weight = models.IntegerField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "psea_rating"


class ReportsAppliedindicator(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    context_code = models.CharField(max_length=50, blank=True, null=True)
    assumptions = models.TextField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    indicator = models.ForeignKey(
        "ReportsIndicatorblueprint",
        models.DO_NOTHING,
        related_name="ReportsAppliedindicator_indicator",
        blank=True,
        null=True,
    )
    lower_result = models.ForeignKey(
        "ReportsLowerresult", models.DO_NOTHING, related_name="ReportsAppliedindicator_lower_result"
    )
    means_of_verification = models.CharField(max_length=255, blank=True, null=True)
    cluster_indicator_id = models.IntegerField(blank=True, null=True)
    cluster_indicator_title = models.CharField(max_length=1024, blank=True, null=True)
    cluster_name = models.CharField(max_length=512, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    response_plan_name = models.CharField(max_length=1024, blank=True, null=True)
    section = models.ForeignKey(
        "ReportsSector", models.DO_NOTHING, related_name="ReportsAppliedindicator_section", blank=True, null=True
    )
    is_active = models.BooleanField()
    is_high_frequency = models.BooleanField()
    baseline = models.JSONField(blank=True, null=True)
    denominator_label = models.CharField(max_length=256, blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    measurement_specifications = models.TextField(blank=True, null=True)
    numerator_label = models.CharField(max_length=256, blank=True, null=True)
    target = models.JSONField()

    class Meta:
        managed = False
        db_table = "reports_appliedindicator"
        unique_together = (("indicator", "lower_result"),)


class ReportsAppliedindicatorDisaggregation(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    appliedindicator = models.ForeignKey(
        ReportsAppliedindicator,
        models.DO_NOTHING,
        related_name="ReportsAppliedindicatorDisaggregation_appliedindicator",
    )
    disaggregation = models.ForeignKey(
        "ReportsDisaggregation", models.DO_NOTHING, related_name="ReportsAppliedindicatorDisaggregation_disaggregation"
    )

    class Meta:
        managed = False
        db_table = "reports_appliedindicator_disaggregation"
        unique_together = (("appliedindicator", "disaggregation"),)


class ReportsAppliedindicatorLocations(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    appliedindicator = models.ForeignKey(
        ReportsAppliedindicator, models.DO_NOTHING, related_name="ReportsAppliedindicatorLocations_appliedindicator"
    )
    location = models.ForeignKey(
        LocationsLocation, models.DO_NOTHING, related_name="ReportsAppliedindicatorLocations_location"
    )

    class Meta:
        managed = False
        db_table = "reports_appliedindicator_locations"
        unique_together = (("appliedindicator", "location"),)


class ReportsCountryprogramme(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    wbs = models.CharField(unique=True, max_length=30)
    from_date = models.DateField()
    to_date = models.DateField()
    invalid = models.BooleanField()

    class Meta:
        managed = False
        db_table = "reports_countryprogramme"


class ReportsDisaggregation(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "reports_disaggregation"


class ReportsDisaggregationvalue(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    value = models.CharField(max_length=20)
    active = models.BooleanField()
    disaggregation = models.ForeignKey(
        ReportsDisaggregation, models.DO_NOTHING, related_name="ReportsDisaggregationvalue_disaggregation"
    )

    class Meta:
        managed = False
        db_table = "reports_disaggregationvalue"


class ReportsIndicator(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1024)
    code = models.CharField(max_length=50, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    sector_total = models.IntegerField(blank=True, null=True)
    current = models.IntegerField(blank=True, null=True)
    sector_current = models.IntegerField(blank=True, null=True)
    view_on_dashboard = models.BooleanField()
    result = models.ForeignKey(
        "ReportsResult", models.DO_NOTHING, related_name="ReportsIndicator_result", blank=True, null=True
    )
    sector = models.ForeignKey(
        "ReportsSector", models.DO_NOTHING, related_name="ReportsIndicator_sector", blank=True, null=True
    )
    unit = models.ForeignKey(
        "ReportsUnit", models.DO_NOTHING, related_name="ReportsIndicator_unit", blank=True, null=True
    )
    baseline = models.CharField(max_length=255, blank=True, null=True)
    ram_indicator = models.BooleanField()
    target = models.CharField(max_length=255, blank=True, null=True)
    assumptions = models.TextField(blank=True, null=True)
    active = models.BooleanField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "reports_indicator"
        unique_together = (("name", "result", "sector"),)


class ReportsIndicatorblueprint(models.TenantModel):
    id = models.IntegerField(primary_key=True)
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
        db_table = "reports_indicatorblueprint"


class ReportsInterventionactivity(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=150)
    context_details = models.TextField(blank=True, null=True)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2)
    cso_cash = models.DecimalField(max_digits=20, decimal_places=2)
    result = models.ForeignKey(
        "ReportsLowerresult", models.DO_NOTHING, related_name="ReportsInterventionactivity_result"
    )
    code = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "reports_interventionactivity"


class ReportsInterventionactivityTimeFrames(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    interventionactivity = models.ForeignKey(
        ReportsInterventionactivity,
        models.DO_NOTHING,
        related_name="ReportsInterventionactivityTimeFrames_interventionactivity",
    )
    interventiontimeframe = models.ForeignKey(
        "ReportsInterventiontimeframe",
        models.DO_NOTHING,
        related_name="ReportsInterventionactivityTimeFrames_interventiontimeframe",
    )

    class Meta:
        managed = False
        db_table = "reports_interventionactivity_time_frames"
        unique_together = (("interventionactivity", "interventiontimeframe"),)


class ReportsInterventionactivityitem(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=150)
    unicef_cash = models.DecimalField(max_digits=20, decimal_places=2)
    cso_cash = models.DecimalField(max_digits=20, decimal_places=2)
    activity = models.ForeignKey(
        ReportsInterventionactivity, models.DO_NOTHING, related_name="ReportsInterventionactivityitem_activity"
    )
    no_units = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.CharField(max_length=150)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reports_interventionactivityitem"


class ReportsInterventiontimeframe(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="ReportsInterventiontimeframe_intervention"
    )
    quarter = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = "reports_interventiontimeframe"


class ReportsLowerresult(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500)
    code = models.CharField(max_length=50, blank=True, null=True)
    result_link = models.ForeignKey(
        PartnersInterventionresultlink, models.DO_NOTHING, related_name="ReportsLowerresult_result_link"
    )
    created = models.DateTimeField()
    modified = models.DateTimeField()
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "reports_lowerresult"
        unique_together = (("code", "result_link"),)


class ReportsOffice(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = "reports_office"


class ReportsQuarter(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    year = models.CharField(max_length=4)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "reports_quarter"


class ReportsReportingrequirement(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    due_date = models.DateField()
    report_type = models.CharField(max_length=50)
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="ReportsReportingrequirement_intervention"
    )

    class Meta:
        managed = False
        db_table = "reports_reportingrequirement"


class ReportsResult(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    code = models.CharField(max_length=50, blank=True, null=True)
    result_type = models.ForeignKey("ReportsResulttype", models.DO_NOTHING, related_name="ReportsResult_result_type")
    sector = models.ForeignKey(
        "ReportsSector", models.DO_NOTHING, related_name="ReportsResult_sector", blank=True, null=True
    )
    gic_code = models.CharField(max_length=8, blank=True, null=True)
    gic_name = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_tag = models.BooleanField()
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey("self", models.DO_NOTHING, related_name="ReportsResult_parent", blank=True, null=True)
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
    country_programme = models.ForeignKey(
        ReportsCountryprogramme,
        models.DO_NOTHING,
        related_name="ReportsResult_country_programme",
        blank=True,
        null=True,
    )
    created = models.DateTimeField()
    modified = models.DateTimeField()
    humanitarian_marker_code = models.CharField(max_length=255, blank=True, null=True)
    humanitarian_marker_name = models.CharField(max_length=255, blank=True, null=True)
    programme_area_code = models.CharField(max_length=16, blank=True, null=True)
    programme_area_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reports_result"
        unique_together = (("country_programme", "wbs"),)


class ReportsResulttype(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "reports_resulttype"


class ReportsSector(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=128)
    description = models.CharField(max_length=256, blank=True, null=True)
    alternate_id = models.IntegerField(blank=True, null=True)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    dashboard = models.BooleanField()
    color = models.CharField(max_length=7, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "reports_sector"


class ReportsSpecialreportingrequirement(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    description = models.CharField(max_length=256)
    due_date = models.DateField()
    intervention = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="ReportsSpecialreportingrequirement_intervention"
    )

    class Meta:
        managed = False
        db_table = "reports_specialreportingrequirement"


class ReportsUnit(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = "reports_unit"


class ReportsUsertenantprofile(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    office = models.ForeignKey(
        ReportsOffice, models.DO_NOTHING, related_name="ReportsUsertenantprofile_office", blank=True, null=True
    )
    profile = models.OneToOneField(
        "UsersUserprofile", models.DO_NOTHING, related_name="ReportsUsertenantprofile_profile"
    )

    class Meta:
        managed = False
        db_table = "reports_usertenantprofile"


class SnapshotActivity(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    target_object_id = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
    data = models.JSONField()
    change = models.JSONField()
    by_user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="SnapshotActivity_by_user")
    target_content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, related_name="SnapshotActivity_target_content_type"
    )

    class Meta:
        managed = False
        db_table = "snapshot_activity"


class T2FItineraryitem(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    overnight_travel = models.BooleanField()
    mode_of_travel = models.CharField(max_length=5)
    dsa_region = models.ForeignKey(
        "PublicsDsaregion", models.DO_NOTHING, related_name="T2FItineraryitem_dsa_region", blank=True, null=True
    )
    travel = models.ForeignKey("T2FTravel", models.DO_NOTHING, related_name="T2FItineraryitem_travel")
    field_order = models.IntegerField(db_column="_order")  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = "t2f_itineraryitem"


class T2FItineraryitemAirlines(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    itineraryitem = models.ForeignKey(
        T2FItineraryitem, models.DO_NOTHING, related_name="T2FItineraryitemAirlines_itineraryitem"
    )
    airlinecompany = models.ForeignKey(
        "PublicsAirlinecompany", models.DO_NOTHING, related_name="T2FItineraryitemAirlines_airlinecompany"
    )

    class Meta:
        managed = False
        db_table = "t2f_itineraryitem_airlines"
        unique_together = (("airlinecompany", "itineraryitem"),)


class T2FTravel(models.TenantModel):
    id = models.IntegerField(primary_key=True)
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
    international_travel = models.BooleanField(blank=True, null=True)
    ta_required = models.BooleanField(blank=True, null=True)
    reference_number = models.CharField(unique=True, max_length=12)
    hidden = models.BooleanField()
    mode_of_travel = models.TextField(blank=True, null=True)  # This field type is a guess.
    estimated_travel_cost = models.DecimalField(max_digits=20, decimal_places=4)
    is_driver = models.BooleanField()
    preserved_expenses_local = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    approved_cost_traveler = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    approved_cost_travel_agencies = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    currency = models.ForeignKey(
        "PublicsCurrency", models.DO_NOTHING, related_name="T2FTravel_currency", blank=True, null=True
    )
    office = models.ForeignKey(ReportsOffice, models.DO_NOTHING, related_name="T2FTravel_office", blank=True, null=True)
    supervisor = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="T2FTravel_supervisor", blank=True, null=True
    )
    traveler = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="T2FTravel_traveler", blank=True, null=True
    )
    first_submission_date = models.DateTimeField(blank=True, null=True)
    preserved_expenses_usd = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    section = models.ForeignKey(
        ReportsSector, models.DO_NOTHING, related_name="T2FTravel_section", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t2f_travel"


class T2FTravelactivity(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    travel_type = models.CharField(max_length=64)
    date = models.DateField(blank=True, null=True)
    partner = models.ForeignKey(
        PartnersPartnerorganization, models.DO_NOTHING, related_name="T2FTravelactivity_partner", blank=True, null=True
    )
    partnership = models.ForeignKey(
        PartnersIntervention, models.DO_NOTHING, related_name="T2FTravelactivity_partnership", blank=True, null=True
    )
    primary_traveler = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="T2FTravelactivity_primary_traveler"
    )
    result = models.ForeignKey(
        ReportsResult, models.DO_NOTHING, related_name="T2FTravelactivity_result", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "t2f_travelactivity"


class T2FTravelactivityLocations(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    travelactivity = models.ForeignKey(
        T2FTravelactivity, models.DO_NOTHING, related_name="T2FTravelactivityLocations_travelactivity"
    )
    location = models.ForeignKey(
        LocationsLocation, models.DO_NOTHING, related_name="T2FTravelactivityLocations_location"
    )

    class Meta:
        managed = False
        db_table = "t2f_travelactivity_locations"
        unique_together = (("location", "travelactivity"),)


class T2FTravelactivityTravels(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    travelactivity = models.ForeignKey(
        T2FTravelactivity, models.DO_NOTHING, related_name="T2FTravelactivityTravels_travelactivity"
    )
    travel = models.ForeignKey(T2FTravel, models.DO_NOTHING, related_name="T2FTravelactivityTravels_travel")

    class Meta:
        managed = False
        db_table = "t2f_travelactivity_travels"
        unique_together = (("travel", "travelactivity"),)


class T2FTravelattachment(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    file = models.CharField(max_length=255, blank=True, null=True)
    travel = models.ForeignKey(T2FTravel, models.DO_NOTHING, related_name="T2FTravelattachment_travel")

    class Meta:
        managed = False
        db_table = "t2f_travelattachment"


class TpmTpmactivity(models.TenantModel):
    activity_ptr = models.OneToOneField(
        ActivitiesActivity, models.DO_NOTHING, related_name="TpmTpmactivity_activity_ptr"
    )
    additional_information = models.TextField()
    is_pv = models.BooleanField()
    tpm_visit = models.ForeignKey("TpmTpmvisit", models.DO_NOTHING, related_name="TpmTpmactivity_tpm_visit")
    section = models.ForeignKey(ReportsSector, models.DO_NOTHING, related_name="TpmTpmactivity_section")

    class Meta:
        managed = False
        db_table = "tpm_tpmactivity"


class TpmTpmactivityOffices(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    tpmactivity = models.ForeignKey(TpmTpmactivity, models.DO_NOTHING, related_name="TpmTpmactivityOffices_tpmactivity")
    office = models.ForeignKey(ReportsOffice, models.DO_NOTHING, related_name="TpmTpmactivityOffices_office")

    class Meta:
        managed = False
        db_table = "tpm_tpmactivity_offices"
        unique_together = (("office", "tpmactivity"),)


class TpmTpmactivityUnicefFocalPoints(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    tpmactivity = models.ForeignKey(
        TpmTpmactivity, models.DO_NOTHING, related_name="TpmTpmactivityUnicefFocalPoints_tpmactivity"
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="TpmTpmactivityUnicefFocalPoints_user")

    class Meta:
        managed = False
        db_table = "tpm_tpmactivity_unicef_focal_points"
        unique_together = (("tpmactivity", "user"),)


class TpmTpmvisit(models.TenantModel):
    id = models.IntegerField(primary_key=True)
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
    tpm_partner = models.ForeignKey(
        "TpmpartnersTpmpartner", models.DO_NOTHING, related_name="TpmTpmvisit_tpm_partner", blank=True, null=True
    )
    cancel_comment = models.TextField()
    author = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="TpmTpmvisit_author", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "tpm_tpmvisit"


class TpmTpmvisitTpmPartnerFocalPoints(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    tpmvisit = models.ForeignKey(
        TpmTpmvisit, models.DO_NOTHING, related_name="TpmTpmvisitTpmPartnerFocalPoints_tpmvisit"
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="TpmTpmvisitTpmPartnerFocalPoints_user")

    class Meta:
        managed = False
        db_table = "tpm_tpmvisit_tpm_partner_focal_points"
        unique_together = (("tpmvisit", "user"),)


class TpmTpmvisitreportrejectcomment(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    rejected_at = models.DateTimeField()
    reject_reason = models.TextField()
    tpm_visit = models.ForeignKey(
        TpmTpmvisit, models.DO_NOTHING, related_name="TpmTpmvisitreportrejectcomment_tpm_visit"
    )

    class Meta:
        managed = False
        db_table = "tpm_tpmvisitreportrejectcomment"


class TravelActivity(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    activity_date = models.DateField()
    activity_type = models.CharField(max_length=64)
    location = models.ForeignKey(
        LocationsLocation, models.DO_NOTHING, related_name="TravelActivity_location", blank=True, null=True
    )
    monitoring_activity = models.ForeignKey(
        FieldMonitoringPlanningMonitoringactivity,
        models.DO_NOTHING,
        related_name="TravelActivity_monitoring_activity",
        blank=True,
        null=True,
    )
    partner = models.ForeignKey(
        PartnersPartnerorganization, models.DO_NOTHING, related_name="TravelActivity_partner", blank=True, null=True
    )
    section = models.ForeignKey(
        ReportsSector, models.DO_NOTHING, related_name="TravelActivity_section", blank=True, null=True
    )
    trip = models.ForeignKey("TravelTrip", models.DO_NOTHING, related_name="TravelActivity_trip")

    class Meta:
        managed = False
        db_table = "travel_activity"


class TravelItineraryitem(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    travel_method = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    trip = models.ForeignKey("TravelTrip", models.DO_NOTHING, related_name="TravelItineraryitem_trip")
    monitoring_activity = models.ForeignKey(
        FieldMonitoringPlanningMonitoringactivity,
        models.DO_NOTHING,
        related_name="TravelItineraryitem_monitoring_activity",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "travel_itineraryitem"


class TravelReport(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    narrative = models.TextField()
    trip = models.OneToOneField("TravelTrip", models.DO_NOTHING, related_name="TravelReport_trip")

    class Meta:
        managed = False
        db_table = "travel_report"


class TravelTrip(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    reference_number = models.CharField(unique=True, max_length=100)
    status = models.CharField(max_length=30)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    office = models.ForeignKey(
        ReportsOffice, models.DO_NOTHING, related_name="TravelTrip_office", blank=True, null=True
    )
    section = models.ForeignKey(
        ReportsSector, models.DO_NOTHING, related_name="TravelTrip_section", blank=True, null=True
    )
    supervisor = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="TravelTrip_supervisor", blank=True, null=True
    )
    traveller = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="TravelTrip_traveller")
    user_info_text = models.JSONField()
    additional_notes = models.TextField(blank=True, null=True)
    not_as_planned = models.BooleanField()

    class Meta:
        managed = False
        db_table = "travel_trip"


class TravelTripstatushistory(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=30)
    comment = models.TextField()
    trip = models.ForeignKey(TravelTrip, models.DO_NOTHING, related_name="TravelTripstatushistory_trip")

    class Meta:
        managed = False
        db_table = "travel_tripstatushistory"


class UnicefAttachmentsAttachment(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    file = models.CharField(max_length=1024, blank=True, null=True)
    hyperlink = models.CharField(max_length=1000)
    object_id = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=64)
    content_type = models.ForeignKey(
        "DjangoContentType",
        models.DO_NOTHING,
        related_name="UnicefAttachmentsAttachment_content_type",
        blank=True,
        null=True,
    )
    file_type = models.ForeignKey(
        "UnicefAttachmentsFiletype",
        models.DO_NOTHING,
        related_name="UnicefAttachmentsAttachment_file_type",
        blank=True,
        null=True,
    )
    uploaded_by = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, related_name="UnicefAttachmentsAttachment_uploaded_by", blank=True, null=True
    )
    ip_address = models.GenericIPAddressField()

    class Meta:
        managed = False
        db_table = "unicef_attachments_attachment"


class UnicefAttachmentsAttachmentflat(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    object_link = models.CharField(max_length=200)
    file_type = models.CharField(max_length=100)
    file_link = models.CharField(max_length=1024)
    filename = models.CharField(max_length=1024)
    uploaded_by = models.CharField(max_length=255)
    created = models.CharField(max_length=50)
    attachment = models.ForeignKey(
        UnicefAttachmentsAttachment, models.DO_NOTHING, related_name="UnicefAttachmentsAttachmentflat_attachment"
    )
    ip_address = models.GenericIPAddressField()

    class Meta:
        managed = False
        db_table = "unicef_attachments_attachmentflat"


class UnicefAttachmentsAttachmentlink(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    object_id = models.IntegerField(blank=True, null=True)
    attachment = models.ForeignKey(
        UnicefAttachmentsAttachment, models.DO_NOTHING, related_name="UnicefAttachmentsAttachmentlink_attachment"
    )
    content_type = models.ForeignKey(
        "DjangoContentType",
        models.DO_NOTHING,
        related_name="UnicefAttachmentsAttachmentlink_content_type",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "unicef_attachments_attachmentlink"


class UnicefAttachmentsFiletype(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    order = models.IntegerField()
    name = models.CharField(max_length=64)
    label = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    group = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "unicef_attachments_filetype"
        unique_together = (("code", "name"),)


class UnicefLocationsCartodbtable(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=254)
    api_key = models.CharField(max_length=254)
    table_name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254)
    name_col = models.CharField(max_length=254)
    pcode_col = models.CharField(max_length=254)
    parent_code_col = models.CharField(max_length=254)
    color = models.CharField(max_length=7)
    level = models.IntegerField()
    lft = models.IntegerField()
    parent = models.ForeignKey(
        "self", models.DO_NOTHING, related_name="UnicefLocationsCartodbtable_parent", blank=True, null=True
    )
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    remap_table_name = models.CharField(max_length=254, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    admin_level = models.SmallIntegerField()
    admin_level_name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = "unicef_locations_cartodbtable"


class UnicefLocationsGatewaytype(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=64)
    admin_level = models.SmallIntegerField(unique=True, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "unicef_locations_gatewaytype"


class UnicefSnapshotActivity(models.TenantModel):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    target_object_id = models.CharField(max_length=255)
    action = models.CharField(max_length=50)
    data = models.JSONField()
    change = models.JSONField()
    by_user = models.ForeignKey("AuthUser", models.DO_NOTHING, related_name="UnicefSnapshotActivity_by_user")
    target_content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, related_name="UnicefSnapshotActivity_target_content_type"
    )

    class Meta:
        managed = False
        db_table = "unicef_snapshot_activity"
