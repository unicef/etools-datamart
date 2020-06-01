from django.contrib.admin import ModelAdmin, register

from etools_datamart.apps.core.admin_mixins import DatamartSourceModelAdmin

from . import models


@register(models.AccountUser)
class AccountUserAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.AccountUserGroups)
class AccountUserGroupsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.AccountUserprofile)
class AccountUserprofileAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.AgencyAgency)
class AgencyAgencyAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.AgencyAgencymember)
class AgencyAgencymemberAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.AgencyAgencyoffice)
class AgencyAgencyofficeAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.AgencyAgencyprofile)
class AgencyAgencyprofileAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.AgencyOtheragency)
class AgencyOtheragencyAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.AuthGroup)
class AuthGroupAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.CommonAdminlevel1)
class CommonAdminlevel1Admin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.CommonCommonfile)
class CommonCommonfileAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.CommonPoint)
class CommonPointAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.CommonSector)
class CommonSectorAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.CommonSpecialization)
class CommonSpecializationAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.DjangoContentType)
class DjangoContentTypeAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.DjangoSite)
class DjangoSiteAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ExternalsPartnervendornumber)
class ExternalsPartnervendornumberAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ExternalsUnicefvendordata)
class ExternalsUnicefvendordataAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.NotificationNotification)
class NotificationNotificationAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.NotificationNotifieduser)
class NotificationNotifieduserAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartner)
class PartnerPartnerAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerLocationFieldOffices)
class PartnerPartnerLocationFieldOfficesAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerauditassessment)
class PartnerPartnerauditassessmentAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerauditreport)
class PartnerPartnerauditreportAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerauthorisedofficer)
class PartnerPartnerauthorisedofficerAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerbudget)
class PartnerPartnerbudgetAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnercapacityassessment)
class PartnerPartnercapacityassessmentAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnercollaborationevidence)
class PartnerPartnercollaborationevidenceAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnercollaborationpartnership)
class PartnerPartnercollaborationpartnershipAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerdirector)
class PartnerPartnerdirectorAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerexperience)
class PartnerPartnerexperienceAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerfunding)
class PartnerPartnerfundingAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnergoverningdocument)
class PartnerPartnergoverningdocumentAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerheadorganization)
class PartnerPartnerheadorganizationAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerinternalcontrol)
class PartnerPartnerinternalcontrolAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnermailingaddress)
class PartnerPartnermailingaddressAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnermandatemission)
class PartnerPartnermandatemissionAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnermember)
class PartnerPartnermemberAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerotherinfo)
class PartnerPartnerotherinfoAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerpolicyarea)
class PartnerPartnerpolicyareaAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerprofile)
class PartnerPartnerprofileAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerregistrationdocument)
class PartnerPartnerregistrationdocumentAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerreporting)
class PartnerPartnerreportingAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerreview)
class PartnerPartnerreviewAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectApplication)
class ProjectApplicationAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectApplicationLocationsProposalOfEoi)
class ProjectApplicationLocationsProposalOfEoiAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectApplicationfeedback)
class ProjectApplicationfeedbackAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectAssessment)
class ProjectAssessmentAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectClarificationrequestanswerfile)
class ProjectClarificationrequestanswerfileAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectClarificationrequestquestion)
class ProjectClarificationrequestquestionAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectEoi)
class ProjectEoiAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectEoiFocalPoints)
class ProjectEoiFocalPointsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectEoiInvitedPartners)
class ProjectEoiInvitedPartnersAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectEoiLocations)
class ProjectEoiLocationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectEoiReviewers)
class ProjectEoiReviewersAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectEoiSpecializations)
class ProjectEoiSpecializationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectEoiattachment)
class ProjectEoiattachmentAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ProjectPin)
class ProjectPinAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ReviewPartnerflag)
class ReviewPartnerflagAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ReviewPartnerverification)
class ReviewPartnerverificationAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.SanctionslistSanctioneditem)
class SanctionslistSanctioneditemAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.SanctionslistSanctionedname)
class SanctionslistSanctionednameAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.SanctionslistSanctionednamematch)
class SanctionslistSanctionednamematchAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.SequencesSequence)
class SequencesSequenceAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []

