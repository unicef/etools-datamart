from django.contrib.admin import register

from etools_datamart.apps.multitenant.admin import EToolsModelAdmin, TenantModelAdmin

from . import models


@register(models.AuthUser)
class AuthUserAdmin(EToolsModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


@register(models.UsersUserprofile)
class UsersUserprofileAdmin(EToolsModelAdmin):
    list_display = ('user', 'country', 'office')
    search_fields = ('user__username', 'user__email')


# @register(models.ActionPointsActionpoint)
# class ActionPoint(TenantModelAdmin):
#     pass


@register(models.ActivitiesActivity)
class ActivitiesActivityAdmin(TenantModelAdmin):
    pass


@register(models.PartnersPartnerorganization)
class PartnerOrganizationAdmin(TenantModelAdmin):
    list_display = ('vendor_number', 'partner_type', 'name', 'short_name', 'schema')
    search_fields = ('name',)
    # list_filter = ('schema',)


@register(models.PartnersAssessment)
class PartnersAssessmentAdmin(TenantModelAdmin):
    pass


#
# @register(models.PartnersAgreement)
# class PartnersAgreementAdmin(TenantModelAdmin):
#     search_fields = ('partner__name',)
#     list_display = ('agreement_number', 'agreement_type', 'partner', 'schema')
#
#     # list_filter = ('agreement_type', )
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('partner')


@register(models.AuditEngagement)
class AuditEngagementAdmin(TenantModelAdmin):
    pass


@register(models.PartnersIntervention)
class PartnersInterventionAdmin(TenantModelAdmin):
    list_display = ('number', 'title', 'document_type', 'schema')
    # list_filter = ('document_type',)


@register(models.T2FTravel)
class T2FTravelAdmin(TenantModelAdmin):
    list_display = ("id", "schema", "status", "purpose")


@register(models.ReportsAppliedindicator)
class ReportsAppliedindicatorAdmin(TenantModelAdmin):
    pass


@register(models.ReportsResult)
class ReportsResultAdmin(TenantModelAdmin):
    list_display = ('name', 'code', 'result_type',)


@register(models.ReportsResulttype)
class ReportsResulttypeAdmin(TenantModelAdmin):
    list_display = ('id', 'name', 'schema')


@register(models.PartnersPlannedengagement)
class PartnersPlannedEngagementAdmin(TenantModelAdmin):
    pass


@register(models.FundsFundsreservationheader)
class FundsReservationHeaderAdmin(TenantModelAdmin):
    pass


@register(models.FundsFundsreservationitem)
class FundsreservationitemAdmin(TenantModelAdmin):
    pass


@register(models.HactAggregatehact)
class HactAggregatehactAdmin(TenantModelAdmin):
    list_display = ('schema', 'year',)


@register(models.TpmTpmvisit)
class TpmTpmvisitAdmin(TenantModelAdmin):
    pass


@register(models.UsersCountry)
class UsersCountryAdmin(EToolsModelAdmin):
    list_display = ('name', 'schema_name', 'business_area_code', 'country_short_code')
    search_fields = ('name', 'schema_name', 'business_area_code')


@register(models.LocationsLocation)
class LocationsLocationAdmin(TenantModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)


# UnicefAttachments

@register(models.UnicefAttachmentsAttachment)
class UnicefAttachmentsAttachmentAdmin(TenantModelAdmin):
    list_display = ('code', 'file')


@register(models.UnicefAttachmentsAttachmentflat)
class UnicefAttachmentsAttachmentflatAdmin(TenantModelAdmin):
    list_display = ('object_link', 'file_type', 'file_link', 'filename')


@register(models.UnicefAttachmentsAttachmentlink)
class UnicefAttachmentsAttachmentlinkAdmin(TenantModelAdmin):
    list_display = ('object_id', 'attachment',)
