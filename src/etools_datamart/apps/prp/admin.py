from django.contrib.admin import ModelAdmin

from etools_datamart.apps.core.admin_mixins import DatamartSourceModelAdmin


class AccountUserAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class AccountUserGroupsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class AccountUserUserPermissionsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class AccountUserprofileAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class AuthtokenTokenAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class ClusterClusterAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class ClusterClusteractivityAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class ClusterClusteractivityLocationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class ClusterClusterobjectiveAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class ClusterClusterobjectiveLocationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class CoreCartodbtableAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class CoreCountryAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class CoreGatewaytypeAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class CoreLocationAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class CorePrproleAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class CoreResponseplanAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class CoreWorkspaceAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class CoreWorkspaceCountriesAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class DjangoAdminLogAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class DjangoContentTypeAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class DjangoMigrationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class DjangoSiteAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class IndicatorDisaggregationAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class IndicatorDisaggregationvalueAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class IndicatorIndicatorblueprintAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class IndicatorIndicatorlocationdataAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class IndicatorIndicatorreportAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class IndicatorReportableAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class IndicatorReportableDisaggregationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class IndicatorReportablelocationgoalAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class IndicatorReportingentityAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class PartnerPartnerAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class PartnerPartnerClustersAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class PartnerPartneractivityAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class PartnerPartneractivityLocationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class PartnerPartneractivityprojectcontextAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class PartnerPartnerprojectAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class PartnerPartnerprojectAdditionalPartnersAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class PartnerPartnerprojectClustersAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class PartnerPartnerprojectLocationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class PartnerPartnerprojectfundingAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefLowerleveloutputAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefNotificationNotificationAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefPdresultlinkAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefPersonAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefProgrammedocumentAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefProgrammedocumentPartnerFocalPointAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefProgrammedocumentSectionsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefProgrammedocumentUnicefFocalPointAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefProgrammedocumentUnicefOfficersAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefProgressreportAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefProgressreportattachmentAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefReportingperioddatesAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


class UnicefSectionAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []
