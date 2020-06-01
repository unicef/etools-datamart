# flake8: noqa F405.
# This is an auto-generated UNPP model module.
# Generated on 2020-06-01 16:55:50.239245
from django.contrib.gis.db import models

from etools_datamart.apps.core.readonly import ReadOnlyModel


class AccountUser(ReadOnlyModel):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    email = models.CharField(unique=True, max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    fullname = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_user'
        app_label = 'unpp'


class AccountUserGroups(ReadOnlyModel):
    user = models.ForeignKey(AccountUser, models.PROTECT, related_name='AccountUserGroups_user')
    group = models.ForeignKey('unpp.AuthGroup', models.PROTECT, related_name='AccountUserGroups_group')

    class Meta:
        managed = False
        db_table = 'account_user_groups'
        unique_together = (('user', 'group'),)
        app_label = 'unpp'


class AccountUserprofile(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user = models.OneToOneField(AccountUser, models.PROTECT, related_name='AccountUserprofile_user')
    notification_frequency = models.TextField(blank=True, null=True)
    accepted_tos = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'account_userprofile'
        app_label = 'unpp'


class AgencyAgency(ReadOnlyModel):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'agency_agency'
        app_label = 'unpp'


class AgencyAgencymember(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    office = models.ForeignKey('unpp.AgencyAgencyoffice', models.PROTECT, related_name='AgencyAgencymember_office')
    user = models.ForeignKey(AccountUser, models.PROTECT, related_name='AgencyAgencymember_user')
    telephone = models.CharField(max_length=255, blank=True, null=True)
    role = models.TextField()

    class Meta:
        managed = False
        db_table = 'agency_agencymember'
        unique_together = (('user', 'office'),)
        app_label = 'unpp'


class AgencyAgencyoffice(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    agency = models.ForeignKey(AgencyAgency, models.PROTECT, related_name='AgencyAgencyoffice_agency')
    country = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'agency_agencyoffice'
        unique_together = (('agency', 'country'),)
        app_label = 'unpp'


class AgencyAgencyprofile(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    eoi_template = models.CharField(max_length=100)
    agency = models.OneToOneField(AgencyAgency, models.PROTECT, related_name='AgencyAgencyprofile_agency')

    class Meta:
        managed = False
        db_table = 'agency_agencyprofile'
        app_label = 'unpp'


class AgencyOtheragency(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'agency_otheragency'
        app_label = 'unpp'


class AuthGroup(ReadOnlyModel):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'
        app_label = 'unpp'


class CommonAdminlevel1(ReadOnlyModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'common_adminlevel1'
        unique_together = (('name', 'country_code'),)
        app_label = 'unpp'


class CommonCommonfile(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    file_field = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'common_commonfile'
        app_label = 'unpp'


class CommonPoint(ReadOnlyModel):
    lat = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    lon = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    admin_level_1 = models.ForeignKey(CommonAdminlevel1, models.PROTECT, related_name='CommonPoint_admin_level_1')

    class Meta:
        managed = False
        db_table = 'common_point'
        app_label = 'unpp'


class CommonSector(ReadOnlyModel):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'common_sector'
        app_label = 'unpp'


class CommonSpecialization(ReadOnlyModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(CommonSector, models.PROTECT, related_name='CommonSpecialization_category')

    class Meta:
        managed = False
        db_table = 'common_specialization'
        app_label = 'unpp'


class DjangoContentType(ReadOnlyModel):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)
        app_label = 'unpp'


class DjangoSite(ReadOnlyModel):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'
        app_label = 'unpp'


class ExternalsPartnervendornumber(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    number = models.TextField()
    agency = models.ForeignKey(AgencyAgency, models.PROTECT, related_name='ExternalsPartnervendornumber_agency')
    partner = models.ForeignKey('unpp.PartnerPartner', models.PROTECT, related_name='ExternalsPartnervendornumber_partner')
    business_area = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'externals_partnervendornumber'
        unique_together = (('agency', 'partner', 'business_area', 'number'),)
        app_label = 'unpp'


class ExternalsUnicefvendordata(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    business_area = models.TextField()
    vendor_number = models.TextField()
    vendor_name = models.TextField()
    total_cash_transfers = models.FloatField()
    cash_transfers_this_year = models.FloatField()
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'externals_unicefvendordata'
        unique_together = (('business_area', 'vendor_number', 'year'),)
        app_label = 'unpp'


class NotificationNotification(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    source = models.TextField()
    content_type = models.ForeignKey(DjangoContentType, models.PROTECT, related_name='NotificationNotification_content_type', blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notification_notification'
        app_label = 'unpp'


class NotificationNotifieduser(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    did_read = models.BooleanField()
    notification = models.ForeignKey(NotificationNotification, models.PROTECT, related_name='NotificationNotifieduser_notification')
    recipient = models.ForeignKey(AccountUser, models.PROTECT, related_name='NotificationNotifieduser_recipient')
    sent_as_email = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'notification_notifieduser'
        unique_together = (('notification', 'recipient'),)
        app_label = 'unpp'


class PartnerPartner(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    legal_name = models.TextField()
    display_type = models.CharField(max_length=3)
    country_code = models.CharField(max_length=2)
    is_active = models.BooleanField()
    hq = models.ForeignKey('self', models.PROTECT, related_name='PartnerPartner_hq', blank=True, null=True)
    country_presence = models.TextField(blank=True, null=True)  # This field type is a guess.
    staff_globally = models.CharField(max_length=3, blank=True, null=True)
    engagement_operate_desc = models.TextField(blank=True, null=True)
    staff_in_country = models.CharField(max_length=3, blank=True, null=True)
    location_of_office = models.ForeignKey(CommonPoint, models.PROTECT, related_name='PartnerPartner_location_of_office', blank=True, null=True)
    more_office_in_country = models.BooleanField(blank=True, null=True)
    is_locked = models.BooleanField()
    declaration = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartner_declaration', blank=True, null=True)
    migrated_from = models.TextField(blank=True, null=True)
    migrated_original_id = models.IntegerField(blank=True, null=True)
    migrated_timestamp = models.DateTimeField(blank=True, null=True)
    legal_name_length = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'partner_partner'
        unique_together = (('legal_name', 'country_code', 'hq'),)
        app_label = 'unpp'


class PartnerPartnerLocationFieldOffices(ReadOnlyModel):
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerLocationFieldOffices_partner')
    point = models.ForeignKey(CommonPoint, models.PROTECT, related_name='PartnerPartnerLocationFieldOffices_point')

    class Meta:
        managed = False
        db_table = 'partner_partner_location_field_offices'
        unique_together = (('partner', 'point'),)
        app_label = 'unpp'


class PartnerPartnerauditassessment(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    regular_audited = models.BooleanField(blank=True, null=True)
    major_accountability_issues_highlighted = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    partner = models.OneToOneField(PartnerPartner, models.PROTECT, related_name='PartnerPartnerauditassessment_partner')
    regular_audited_comment = models.TextField(blank=True, null=True)
    regular_capacity_assessments = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnerauditassessment'
        app_label = 'unpp'


class PartnerPartnerauditreport(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    org_audit = models.CharField(max_length=3, blank=True, null=True)
    link_report = models.CharField(max_length=200, blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerauditreport_partner')
    most_recent_audit_report = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnerauditreport_most_recent_audit_report', blank=True, null=True)
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnerauditreport_created_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnerauditreport'
        app_label = 'unpp'


class PartnerPartnerauthorisedofficer(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    job_title = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerauthorisedofficer_partner')
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnerauthorisedofficer_created_by', blank=True, null=True)
    fullname = models.CharField(max_length=512, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnerauthorisedofficer'
        app_label = 'unpp'


class PartnerPartnerbudget(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    year = models.SmallIntegerField()
    budget = models.CharField(max_length=3, blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerbudget_partner')
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnerbudget_created_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnerbudget'
        unique_together = (('partner', 'year'),)
        app_label = 'unpp'


class PartnerPartnercapacityassessment(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    assessment_type = models.TextField(blank=True, null=True)
    report_url = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnercapacityassessment_created_by', blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnercapacityassessment_partner')
    report_file = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnercapacityassessment_report_file', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnercapacityassessment'
        app_label = 'unpp'


class PartnerPartnercollaborationevidence(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    mode = models.CharField(max_length=3, blank=True, null=True)
    organization_name = models.CharField(max_length=1000, blank=True, null=True)
    date_received = models.DateField(blank=True, null=True)
    evidence_file = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnercollaborationevidence_evidence_file', blank=True, null=True)
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnercollaborationevidence_created_by')
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnercollaborationevidence_partner')
    editable = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'partner_partnercollaborationevidence'
        app_label = 'unpp'


class PartnerPartnercollaborationpartnership(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    description = models.CharField(max_length=10000, blank=True, null=True)
    partner_number = models.CharField(max_length=200, blank=True, null=True)
    agency = models.ForeignKey(AgencyAgency, models.PROTECT, related_name='PartnerPartnercollaborationpartnership_agency', blank=True, null=True)
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnercollaborationpartnership_created_by')
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnercollaborationpartnership_partner')

    class Meta:
        managed = False
        db_table = 'partner_partnercollaborationpartnership'
        unique_together = (('partner', 'agency'),)
        app_label = 'unpp'


class PartnerPartnerdirector(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    job_title = models.CharField(max_length=255, blank=True, null=True)
    authorized = models.BooleanField(blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerdirector_partner')
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnerdirector_created_by', blank=True, null=True)
    fullname = models.CharField(max_length=512, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnerdirector'
        app_label = 'unpp'


class PartnerPartnerexperience(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    years = models.CharField(max_length=3, blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerexperience_partner')
    specialization = models.ForeignKey(CommonSpecialization, models.PROTECT, related_name='PartnerPartnerexperience_specialization', blank=True, null=True)
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnerexperience_created_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnerexperience'
        app_label = 'unpp'


class PartnerPartnerfunding(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    source_core_funding = models.CharField(max_length=5000)
    major_donors = models.TextField(blank=True, null=True)  # This field type is a guess.
    main_donors_list = models.CharField(max_length=5000, blank=True, null=True)
    partner = models.OneToOneField(PartnerPartner, models.PROTECT, related_name='PartnerPartnerfunding_partner')

    class Meta:
        managed = False
        db_table = 'partner_partnerfunding'
        app_label = 'unpp'


class PartnerPartnergoverningdocument(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    editable = models.BooleanField()
    document = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnergoverningdocument_document')
    profile = models.ForeignKey('unpp.PartnerPartnerprofile', models.PROTECT, related_name='PartnerPartnergoverningdocument_profile')
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnergoverningdocument_created_by')

    class Meta:
        managed = False
        db_table = 'partner_partnergoverningdocument'
        app_label = 'unpp'


class PartnerPartnerheadorganization(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    email = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerheadorganization_partner', blank=True, null=True)
    fullname = models.CharField(max_length=512, blank=True, null=True)
    authorized = models.BooleanField(blank=True, null=True)
    board_member = models.BooleanField(blank=True, null=True)
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnerheadorganization_created_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnerheadorganization'
        app_label = 'unpp'


class PartnerPartnerinternalcontrol(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    functional_responsibility = models.CharField(max_length=3)
    segregation_duties = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerinternalcontrol_partner')

    class Meta:
        managed = False
        db_table = 'partner_partnerinternalcontrol'
        unique_together = (('partner', 'functional_responsibility'),)
        app_label = 'unpp'


class PartnerPartnermailingaddress(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    mailing_type = models.CharField(max_length=3)
    street = models.CharField(max_length=1000, blank=True, null=True)
    po_box = models.CharField(max_length=1000, blank=True, null=True)
    city = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=1000, blank=True, null=True)
    telephone = models.CharField(max_length=1000, blank=True, null=True)
    fax = models.CharField(max_length=1000, blank=True, null=True)
    website = models.CharField(max_length=1000, blank=True, null=True)
    org_email = models.CharField(max_length=1000, blank=True, null=True)
    partner = models.OneToOneField(PartnerPartner, models.PROTECT, related_name='PartnerPartnermailingaddress_partner')

    class Meta:
        managed = False
        db_table = 'partner_partnermailingaddress'
        app_label = 'unpp'


class PartnerPartnermandatemission(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    background_and_rationale = models.TextField(blank=True, null=True)
    mandate_and_mission = models.TextField(blank=True, null=True)
    governance_structure = models.TextField(blank=True, null=True)
    governance_hq = models.TextField(blank=True, null=True)
    governance_organigram = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnermandatemission_governance_organigram', blank=True, null=True)
    ethic_safeguard = models.BooleanField(blank=True, null=True)
    ethic_safeguard_policy = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnermandatemission_ethic_safeguard_policy', blank=True, null=True)
    ethic_fraud = models.BooleanField(blank=True, null=True)
    ethic_fraud_policy = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnermandatemission_ethic_fraud_policy', blank=True, null=True)
    population_of_concern = models.BooleanField(blank=True, null=True)
    concern_groups = models.TextField(blank=True, null=True)  # This field type is a guess.
    security_high_risk_locations = models.BooleanField(blank=True, null=True)
    security_high_risk_policy = models.BooleanField(blank=True, null=True)
    security_desc = models.TextField(blank=True, null=True)
    partner = models.OneToOneField(PartnerPartner, models.PROTECT, related_name='PartnerPartnermandatemission_partner')
    ethic_fraud_comment = models.TextField(blank=True, null=True)
    ethic_safeguard_comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnermandatemission'
        app_label = 'unpp'


class PartnerPartnermember(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    title = models.CharField(max_length=255)
    role = models.TextField()
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnermember_partner')
    user = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnermember_user')

    class Meta:
        managed = False
        db_table = 'partner_partnermember'
        unique_together = (('user', 'partner'),)
        app_label = 'unpp'


class PartnerPartnerotherinfo(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    info_to_share = models.TextField(blank=True, null=True)
    org_logo = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnerotherinfo_org_logo', blank=True, null=True)
    confirm_data_updated = models.BooleanField(blank=True, null=True)
    partner = models.OneToOneField(PartnerPartner, models.PROTECT, related_name='PartnerPartnerotherinfo_partner')
    other_doc_1 = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnerotherinfo_other_doc_1', blank=True, null=True)
    other_doc_2 = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnerotherinfo_other_doc_2', blank=True, null=True)
    other_doc_3 = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnerotherinfo_other_doc_3', blank=True, null=True)
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnerotherinfo_created_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnerotherinfo'
        app_label = 'unpp'


class PartnerPartnerpolicyarea(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    area = models.CharField(max_length=3)
    document_policies = models.BooleanField(blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerpolicyarea_partner')
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnerpolicyarea_created_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnerpolicyarea'
        unique_together = (('partner', 'area'),)
        app_label = 'unpp'


class PartnerPartnerprofile(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    alias_name = models.CharField(max_length=255, blank=True, null=True)
    legal_name_change = models.BooleanField(blank=True, null=True)
    former_legal_name = models.CharField(max_length=255, blank=True, null=True)
    working_languages = models.TextField(blank=True, null=True)  # This field type is a guess.
    working_languages_other = models.CharField(max_length=100, blank=True, null=True)
    have_governing_document = models.BooleanField(blank=True, null=True)
    have_management_approach = models.BooleanField(blank=True, null=True)
    management_approach_desc = models.TextField(blank=True, null=True)
    have_system_monitoring = models.BooleanField(blank=True, null=True)
    system_monitoring_desc = models.TextField(blank=True, null=True)
    have_feedback_mechanism = models.BooleanField(blank=True, null=True)
    org_acc_system = models.CharField(max_length=3)
    method_acc = models.CharField(max_length=3)
    have_system_track = models.BooleanField(blank=True, null=True)
    financial_control_system_desc = models.TextField(blank=True, null=True)
    partner = models.OneToOneField(PartnerPartner, models.PROTECT, related_name='PartnerPartnerprofile_partner')
    connectivity = models.BooleanField(blank=True, null=True)
    connectivity_excuse = models.CharField(max_length=5000, blank=True, null=True)
    experienced_staff = models.BooleanField(blank=True, null=True)
    experienced_staff_desc = models.TextField(blank=True, null=True)
    feedback_mechanism_desc = models.TextField(blank=True, null=True)
    acronym = models.CharField(max_length=200, blank=True, null=True)
    partnership_collaborate_institution = models.BooleanField(blank=True, null=True)
    partnership_collaborate_institution_desc = models.CharField(max_length=5000, blank=True, null=True)
    explain = models.TextField(blank=True, null=True)
    have_bank_account = models.BooleanField(blank=True, null=True)
    have_board_directors = models.BooleanField(blank=True, null=True)
    have_separate_bank_account = models.BooleanField(blank=True, null=True)
    missing_registration_document_comment = models.TextField(blank=True, null=True)
    registered_to_operate_in_country = models.BooleanField(blank=True, null=True)
    year_establishment = models.SmallIntegerField(blank=True, null=True)
    have_authorised_officers = models.BooleanField(blank=True, null=True)
    any_accreditation = models.BooleanField(blank=True, null=True)
    any_partnered_with_un = models.BooleanField(blank=True, null=True)
    any_reference = models.BooleanField(blank=True, null=True)
    missing_governing_document_comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_partnerprofile'
        app_label = 'unpp'


class PartnerPartnerregistrationdocument(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    registration_number = models.TextField(blank=True, null=True)
    editable = models.BooleanField()
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    document = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnerregistrationdocument_document')
    profile = models.ForeignKey(PartnerPartnerprofile, models.PROTECT, related_name='PartnerPartnerregistrationdocument_profile')
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnerregistrationdocument_created_by')
    issuing_authority = models.TextField()

    class Meta:
        managed = False
        db_table = 'partner_partnerregistrationdocument'
        app_label = 'unpp'


class PartnerPartnerreporting(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    key_result = models.TextField(blank=True, null=True)
    publish_annual_reports = models.BooleanField(blank=True, null=True)
    last_report = models.DateField(blank=True, null=True)
    report = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='PartnerPartnerreporting_report', blank=True, null=True)
    link_report = models.CharField(max_length=1000, blank=True, null=True)
    partner = models.OneToOneField(PartnerPartner, models.PROTECT, related_name='PartnerPartnerreporting_partner')

    class Meta:
        managed = False
        db_table = 'partner_partnerreporting'
        app_label = 'unpp'


class PartnerPartnerreview(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    display_type = models.CharField(max_length=3)
    performance_pm = models.CharField(max_length=3)
    performance_financial = models.CharField(max_length=3)
    performance_com_eng = models.CharField(max_length=3)
    ethical_concerns = models.BooleanField(blank=True, null=True)
    does_recommend = models.BooleanField(blank=True, null=True)
    comment = models.TextField()
    agency = models.ForeignKey(AgencyAgency, models.PROTECT, related_name='PartnerPartnerreview_agency')
    eoi = models.ForeignKey('unpp.ProjectEoi', models.PROTECT, related_name='PartnerPartnerreview_eoi')
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='PartnerPartnerreview_partner')
    reviewer = models.ForeignKey(AccountUser, models.PROTECT, related_name='PartnerPartnerreview_reviewer')

    class Meta:
        managed = False
        db_table = 'partner_partnerreview'
        app_label = 'unpp'


class ProjectApplication(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    is_unsolicited = models.BooleanField()
    status = models.CharField(max_length=3)
    did_win = models.BooleanField()
    did_accept = models.BooleanField()
    ds_justification_select = models.TextField(blank=True, null=True)  # This field type is a guess.
    justification_reason = models.TextField(blank=True, null=True)
    eoi = models.ForeignKey('unpp.ProjectEoi', models.PROTECT, related_name='ProjectApplication_eoi', blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='ProjectApplication_partner')
    submitter = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectApplication_submitter')
    proposal_of_eoi_details = models.TextField()  # This field type is a guess.
    agency = models.ForeignKey(AgencyAgency, models.PROTECT, related_name='ProjectApplication_agency')
    did_withdraw = models.BooleanField()
    withdraw_reason = models.TextField(blank=True, null=True)
    did_decline = models.BooleanField()
    eoi_converted = models.OneToOneField('unpp.ProjectEoi', models.PROTECT, related_name='ProjectApplication_eoi_converted', blank=True, null=True)
    cn = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='ProjectApplication_cn', blank=True, null=True)
    accept_notification = models.OneToOneField(NotificationNotification, models.PROTECT, related_name='ProjectApplication_accept_notification', blank=True, null=True)
    partner_decision_date = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(blank=True, null=True)
    ds_attachment = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='ProjectApplication_ds_attachment', blank=True, null=True)
    published_timestamp = models.DateTimeField(blank=True, null=True)
    partner_decision_maker = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectApplication_partner_decision_maker', blank=True, null=True)
    agency_decision_date = models.DateField(blank=True, null=True)
    agency_decision_maker = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectApplication_agency_decision_maker', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_application'
        unique_together = (('eoi', 'partner'),)
        app_label = 'unpp'


class ProjectApplicationLocationsProposalOfEoi(ReadOnlyModel):
    application = models.ForeignKey(ProjectApplication, models.PROTECT, related_name='ProjectApplicationLocationsProposalOfEoi_application')
    point = models.ForeignKey(CommonPoint, models.PROTECT, related_name='ProjectApplicationLocationsProposalOfEoi_point')

    class Meta:
        managed = False
        db_table = 'project_application_locations_proposal_of_eoi'
        unique_together = (('application', 'point'),)
        app_label = 'unpp'


class ProjectApplicationfeedback(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    feedback = models.TextField()
    application = models.ForeignKey(ProjectApplication, models.PROTECT, related_name='ProjectApplicationfeedback_application')
    provider = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectApplicationfeedback_provider')

    class Meta:
        managed = False
        db_table = 'project_applicationfeedback'
        app_label = 'unpp'


class ProjectAssessment(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    date_reviewed = models.DateField()
    application = models.ForeignKey(ProjectApplication, models.PROTECT, related_name='ProjectAssessment_application')
    reviewer = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectAssessment_reviewer')
    note = models.TextField(blank=True, null=True)
    scores = models.TextField()  # This field type is a guess.
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectAssessment_created_by')
    modified_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectAssessment_modified_by', blank=True, null=True)
    archived = models.BooleanField()
    is_a_committee_score = models.BooleanField()
    completed = models.BooleanField()
    completed_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_assessment'
        unique_together = (('reviewer', 'application'),)
        app_label = 'unpp'


class ProjectClarificationrequestanswerfile(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    title = models.TextField()
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectClarificationrequestanswerfile_created_by')
    eoi = models.ForeignKey('unpp.ProjectEoi', models.PROTECT, related_name='ProjectClarificationrequestanswerfile_eoi')
    file = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='ProjectClarificationrequestanswerfile_file')

    class Meta:
        managed = False
        db_table = 'project_clarificationrequestanswerfile'
        app_label = 'unpp'


class ProjectClarificationrequestquestion(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    question = models.TextField()
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectClarificationrequestquestion_created_by')
    eoi = models.ForeignKey('unpp.ProjectEoi', models.PROTECT, related_name='ProjectClarificationrequestquestion_eoi')
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='ProjectClarificationrequestquestion_partner')

    class Meta:
        managed = False
        db_table = 'project_clarificationrequestquestion'
        app_label = 'unpp'


class ProjectEoi(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    display_type = models.CharField(max_length=3)
    title = models.CharField(max_length=255)
    cn_template = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=5000)
    other_information = models.CharField(max_length=5000, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    deadline_date = models.DateField(blank=True, null=True)
    notif_results_date = models.DateField(blank=True, null=True)
    has_weighting = models.BooleanField()
    justification = models.TextField(blank=True, null=True)
    agency = models.ForeignKey(AgencyAgency, models.PROTECT, related_name='ProjectEoi_agency')
    agency_office = models.ForeignKey(AgencyAgencyoffice, models.PROTECT, related_name='ProjectEoi_agency_office')
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectEoi_created_by')
    selected_source = models.CharField(max_length=3, blank=True, null=True)
    completed_reason = models.TextField(blank=True, null=True)
    goal = models.CharField(max_length=5000, blank=True, null=True)
    assessments_criteria = models.TextField()  # This field type is a guess.
    completed_date = models.DateTimeField(blank=True, null=True)
    review_summary_attachment = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='ProjectEoi_review_summary_attachment', blank=True, null=True)
    review_summary_comment = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField()
    is_published = models.BooleanField()
    completed_comment = models.TextField(blank=True, null=True)
    completed_retention = models.TextField(blank=True, null=True)
    sent_for_publishing = models.BooleanField()
    published_timestamp = models.DateTimeField()
    displayid = models.TextField(db_column='displayID', unique=True)  # Field name made lowercase.
    sent_for_decision = models.BooleanField()
    preselected_partners = models.TextField()  # This field type is a guess.
    clarification_request_deadline_date = models.DateField(blank=True, null=True)
    population = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'project_eoi'
        app_label = 'unpp'


class ProjectEoiFocalPoints(ReadOnlyModel):
    eoi = models.ForeignKey(ProjectEoi, models.PROTECT, related_name='ProjectEoiFocalPoints_eoi')
    user = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectEoiFocalPoints_user')

    class Meta:
        managed = False
        db_table = 'project_eoi_focal_points'
        unique_together = (('eoi', 'user'),)
        app_label = 'unpp'


class ProjectEoiInvitedPartners(ReadOnlyModel):
    eoi = models.ForeignKey(ProjectEoi, models.PROTECT, related_name='ProjectEoiInvitedPartners_eoi')
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='ProjectEoiInvitedPartners_partner')

    class Meta:
        managed = False
        db_table = 'project_eoi_invited_partners'
        unique_together = (('eoi', 'partner'),)
        app_label = 'unpp'


class ProjectEoiLocations(ReadOnlyModel):
    eoi = models.ForeignKey(ProjectEoi, models.PROTECT, related_name='ProjectEoiLocations_eoi')
    point = models.ForeignKey(CommonPoint, models.PROTECT, related_name='ProjectEoiLocations_point')

    class Meta:
        managed = False
        db_table = 'project_eoi_locations'
        unique_together = (('eoi', 'point'),)
        app_label = 'unpp'


class ProjectEoiReviewers(ReadOnlyModel):
    eoi = models.ForeignKey(ProjectEoi, models.PROTECT, related_name='ProjectEoiReviewers_eoi')
    user = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectEoiReviewers_user')

    class Meta:
        managed = False
        db_table = 'project_eoi_reviewers'
        unique_together = (('eoi', 'user'),)
        app_label = 'unpp'


class ProjectEoiSpecializations(ReadOnlyModel):
    eoi = models.ForeignKey(ProjectEoi, models.PROTECT, related_name='ProjectEoiSpecializations_eoi')
    specialization = models.ForeignKey(CommonSpecialization, models.PROTECT, related_name='ProjectEoiSpecializations_specialization')

    class Meta:
        managed = False
        db_table = 'project_eoi_specializations'
        unique_together = (('eoi', 'specialization'),)
        app_label = 'unpp'


class ProjectEoiattachment(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    description = models.TextField()
    created_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectEoiattachment_created_by')
    eoi = models.ForeignKey(ProjectEoi, models.PROTECT, related_name='ProjectEoiattachment_eoi')
    file = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='ProjectEoiattachment_file')

    class Meta:
        managed = False
        db_table = 'project_eoiattachment'
        app_label = 'unpp'


class ProjectPin(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    eoi = models.ForeignKey(ProjectEoi, models.PROTECT, related_name='ProjectPin_eoi')
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='ProjectPin_partner')
    pinned_by = models.ForeignKey(AccountUser, models.PROTECT, related_name='ProjectPin_pinned_by')

    class Meta:
        managed = False
        db_table = 'project_pin'
        unique_together = (('eoi', 'partner'),)
        app_label = 'unpp'


class ReviewPartnerflag(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    flag_type = models.TextField()
    is_valid = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_phone = models.CharField(max_length=16, blank=True, null=True)
    contact_email = models.CharField(max_length=254, blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='ReviewPartnerflag_partner')
    submitter = models.ForeignKey(AccountUser, models.PROTECT, related_name='ReviewPartnerflag_submitter', blank=True, null=True)
    attachment = models.ForeignKey(CommonCommonfile, models.PROTECT, related_name='ReviewPartnerflag_attachment', blank=True, null=True)
    sanctions_match = models.ForeignKey('unpp.SanctionslistSanctionednamematch', models.PROTECT, related_name='ReviewPartnerflag_sanctions_match', blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    type_history = models.TextField(blank=True, null=True)  # This field type is a guess.
    validation_comment = models.TextField(blank=True, null=True)
    escalation_comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review_partnerflag'
        app_label = 'unpp'


class ReviewPartnerverification(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    is_valid = models.BooleanField()
    is_verified = models.BooleanField()
    is_cert_uploaded = models.BooleanField()
    cert_uploaded_comment = models.TextField(blank=True, null=True)
    is_mm_consistent = models.BooleanField()
    mm_consistent_comment = models.TextField(blank=True, null=True)
    is_indicate_results = models.BooleanField()
    indicate_results_comment = models.TextField(blank=True, null=True)
    is_rep_risk = models.BooleanField()
    rep_risk_comment = models.TextField(blank=True, null=True)
    is_yellow_flag = models.BooleanField()
    yellow_flag_comment = models.TextField(blank=True, null=True)
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='ReviewPartnerverification_partner')
    submitter = models.ForeignKey(AccountUser, models.PROTECT, related_name='ReviewPartnerverification_submitter')

    class Meta:
        managed = False
        db_table = 'review_partnerverification'
        app_label = 'unpp'


class SanctionslistSanctioneditem(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    sanctioned_type = models.CharField(max_length=3)
    is_active = models.BooleanField()
    data_id = models.IntegerField(unique=True)
    listed_on = models.DateField(blank=True, null=True)
    last_updated = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sanctionslist_sanctioneditem'
        app_label = 'unpp'


class SanctionslistSanctionedname(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.TextField()
    is_active = models.BooleanField()
    item = models.ForeignKey(SanctionslistSanctioneditem, models.PROTECT, related_name='SanctionslistSanctionedname_item')

    class Meta:
        managed = False
        db_table = 'sanctionslist_sanctionedname'
        unique_together = (('item', 'name'),)
        app_label = 'unpp'


class SanctionslistSanctionednamematch(ReadOnlyModel):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    can_ignore = models.BooleanField()
    match_type = models.CharField(max_length=3)
    match_text = models.TextField(blank=True, null=True)
    can_ignore_text = models.TextField(blank=True, null=True)
    name = models.ForeignKey(SanctionslistSanctionedname, models.PROTECT, related_name='SanctionslistSanctionednamematch_name')
    partner = models.ForeignKey(PartnerPartner, models.PROTECT, related_name='SanctionslistSanctionednamematch_partner')

    class Meta:
        managed = False
        db_table = 'sanctionslist_sanctionednamematch'
        unique_together = (('name', 'partner'),)
        app_label = 'unpp'


class SequencesSequence(ReadOnlyModel):
    name = models.CharField(primary_key=True, max_length=100)
    last = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sequences_sequence'
        app_label = 'unpp'
