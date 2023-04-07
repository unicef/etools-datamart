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


@register(models.AuthGroup)
class AuthGroupAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.AuthtokenToken)
class AuthtokenTokenAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ClusterCluster)
class ClusterClusterAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ClusterClusteractivity)
class ClusterClusteractivityAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ClusterClusteractivityLocations)
class ClusterClusteractivityLocationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ClusterClusterobjective)
class ClusterClusterobjectiveAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.ClusterClusterobjectiveLocations)
class ClusterClusterobjectiveLocationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.CoreCountry)
class CoreCountryAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.CoreLocation)
class CoreLocationAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.CoreLocationWorkspaces)
class CoreLocationWorkspacesAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.CorePrprole)
class CorePrproleAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.CoreResponseplan)
class CoreResponseplanAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.CoreWorkspace)
class CoreWorkspaceAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.DjangoContentType)
class DjangoContentTypeAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.DjangoSite)
class DjangoSiteAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.IndicatorDisaggregation)
class IndicatorDisaggregationAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.IndicatorDisaggregationvalue)
class IndicatorDisaggregationvalueAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.IndicatorIndicatorblueprint)
class IndicatorIndicatorblueprintAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.IndicatorIndicatorlocationdata)
class IndicatorIndicatorlocationdataAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.IndicatorIndicatorreport)
class IndicatorIndicatorreportAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.IndicatorReportable)
class IndicatorReportableAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = ["content_type"]


@register(models.IndicatorReportableDisaggregations)
class IndicatorReportableDisaggregationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.IndicatorReportablelocationgoal)
class IndicatorReportablelocationgoalAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.IndicatorReportingentity)
class IndicatorReportingentityAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartner)
class PartnerPartnerAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerClusters)
class PartnerPartnerClustersAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartneractivity)
class PartnerPartneractivityAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartneractivityLocations)
class PartnerPartneractivityLocationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartneractivityprojectcontext)
class PartnerPartneractivityprojectcontextAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerproject)
class PartnerPartnerprojectAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerprojectAdditionalPartners)
class PartnerPartnerprojectAdditionalPartnersAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerprojectClusters)
class PartnerPartnerprojectClustersAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerprojectLocations)
class PartnerPartnerprojectLocationsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.PartnerPartnerprojectfunding)
class PartnerPartnerprojectfundingAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefFinalreview)
class UnicefFinalreviewAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefLocationsCartodbtable)
class UnicefLocationsCartodbtableAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefLocationsGatewaytype)
class UnicefLocationsGatewaytypeAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefLowerleveloutput)
class UnicefLowerleveloutputAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefPdresultlink)
class UnicefPdresultlinkAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefPerson)
class UnicefPersonAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefProgrammedocument)
class UnicefProgrammedocumentAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefProgrammedocumentPartnerFocalPoint)
class UnicefProgrammedocumentPartnerFocalPointAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefProgrammedocumentSections)
class UnicefProgrammedocumentSectionsAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefProgrammedocumentUnicefFocalPoint)
class UnicefProgrammedocumentUnicefFocalPointAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefProgrammedocumentUnicefOfficers)
class UnicefProgrammedocumentUnicefOfficersAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefProgressreport)
class UnicefProgressreportAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = ["status"]


@register(models.UnicefProgressreportattachment)
class UnicefProgressreportattachmentAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefReportingperioddates)
class UnicefReportingperioddatesAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []


@register(models.UnicefSection)
class UnicefSectionAdmin(DatamartSourceModelAdmin, ModelAdmin):
    list_filter = []
