from unicef_rest_framework.views import URFReadOnlyModelViewSet

from etools_datamart.api.endpoints.etools import serializers
from etools_datamart.apps.prp import models


class AccountUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountUser
        exclude = ()


class AccountUserViewSet(URFReadOnlyModelViewSet):
    serializer_class = AccountUserSerializer
    queryset = models.AccountUser.objects.all()


class AccountUserGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountUserGroups
        exclude = ()


class AccountUserGroupsViewSet(URFReadOnlyModelViewSet):
    serializer_class = AccountUserGroupsSerializer
    queryset = models.AccountUserGroups.objects.all()


class AccountUserUserPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountUserUserPermissions
        exclude = ()


class AccountUserUserPermissionsViewSet(URFReadOnlyModelViewSet):
    serializer_class = AccountUserUserPermissionsSerializer
    queryset = models.AccountUserUserPermissions.objects.all()


class AccountUserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountUserprofile
        exclude = ()


class AccountUserprofileViewSet(URFReadOnlyModelViewSet):
    serializer_class = AccountUserprofileSerializer
    queryset = models.AccountUserprofile.objects.all()


class AuthtokenTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthtokenToken
        exclude = ()


class AuthtokenTokenViewSet(URFReadOnlyModelViewSet):
    serializer_class = AuthtokenTokenSerializer
    queryset = models.AuthtokenToken.objects.all()


class ClusterClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClusterCluster
        exclude = ()


class ClusterClusterViewSet(URFReadOnlyModelViewSet):
    serializer_class = ClusterClusterSerializer
    queryset = models.ClusterCluster.objects.all()


class ClusterClusteractivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClusterClusteractivity
        exclude = ()


class ClusterClusteractivityViewSet(URFReadOnlyModelViewSet):
    serializer_class = ClusterClusteractivitySerializer
    queryset = models.ClusterClusteractivity.objects.all()


class ClusterClusteractivityLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClusterClusteractivityLocations
        exclude = ()


class ClusterClusteractivityLocationsViewSet(URFReadOnlyModelViewSet):
    serializer_class = ClusterClusteractivityLocationsSerializer
    queryset = models.ClusterClusteractivityLocations.objects.all()


class ClusterClusterobjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClusterClusterobjective
        exclude = ()


class ClusterClusterobjectiveViewSet(URFReadOnlyModelViewSet):
    serializer_class = ClusterClusterobjectiveSerializer
    queryset = models.ClusterClusterobjective.objects.all()


class ClusterClusterobjectiveLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClusterClusterobjectiveLocations
        exclude = ()


class ClusterClusterobjectiveLocationsViewSet(URFReadOnlyModelViewSet):
    serializer_class = ClusterClusterobjectiveLocationsSerializer
    queryset = models.ClusterClusterobjectiveLocations.objects.all()


class CoreCartodbtableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoreCartodbtable
        exclude = ()


class CoreCartodbtableViewSet(URFReadOnlyModelViewSet):
    serializer_class = CoreCartodbtableSerializer
    queryset = models.CoreCartodbtable.objects.all()


class CoreCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoreCountry
        exclude = ()


class CoreCountryViewSet(URFReadOnlyModelViewSet):
    serializer_class = CoreCountrySerializer
    queryset = models.CoreCountry.objects.all()


class CoreGatewaytypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoreGatewaytype
        exclude = ()


class CoreGatewaytypeViewSet(URFReadOnlyModelViewSet):
    serializer_class = CoreGatewaytypeSerializer
    queryset = models.CoreGatewaytype.objects.all()


class CoreLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoreLocation
        exclude = ()


class CoreLocationViewSet(URFReadOnlyModelViewSet):
    serializer_class = CoreLocationSerializer
    queryset = models.CoreLocation.objects.all()


class CorePrproleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CorePrprole
        exclude = ()


class CorePrproleViewSet(URFReadOnlyModelViewSet):
    serializer_class = CorePrproleSerializer
    queryset = models.CorePrprole.objects.all()


class CoreResponseplanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoreResponseplan
        exclude = ()


class CoreResponseplanViewSet(URFReadOnlyModelViewSet):
    serializer_class = CoreResponseplanSerializer
    queryset = models.CoreResponseplan.objects.all()


class CoreWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoreWorkspace
        exclude = ()


class CoreWorkspaceViewSet(URFReadOnlyModelViewSet):
    serializer_class = CoreWorkspaceSerializer
    queryset = models.CoreWorkspace.objects.all()


class CoreWorkspaceCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoreWorkspaceCountries
        exclude = ()


class CoreWorkspaceCountriesViewSet(URFReadOnlyModelViewSet):
    serializer_class = CoreWorkspaceCountriesSerializer
    queryset = models.CoreWorkspaceCountries.objects.all()


class DjangoAdminLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DjangoAdminLog
        exclude = ()


class DjangoAdminLogViewSet(URFReadOnlyModelViewSet):
    serializer_class = DjangoAdminLogSerializer
    queryset = models.DjangoAdminLog.objects.all()


class DjangoContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DjangoContentType
        exclude = ()


class DjangoContentTypeViewSet(URFReadOnlyModelViewSet):
    serializer_class = DjangoContentTypeSerializer
    queryset = models.DjangoContentType.objects.all()


class DjangoMigrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DjangoMigrations
        exclude = ()


class DjangoMigrationsViewSet(URFReadOnlyModelViewSet):
    serializer_class = DjangoMigrationsSerializer
    queryset = models.DjangoMigrations.objects.all()


class DjangoSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DjangoSite
        exclude = ()


class DjangoSiteViewSet(URFReadOnlyModelViewSet):
    serializer_class = DjangoSiteSerializer
    queryset = models.DjangoSite.objects.all()


class IndicatorDisaggregationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatorDisaggregation
        exclude = ()


class IndicatorDisaggregationViewSet(URFReadOnlyModelViewSet):
    serializer_class = IndicatorDisaggregationSerializer
    queryset = models.IndicatorDisaggregation.objects.all()


class IndicatorDisaggregationvalueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatorDisaggregationvalue
        exclude = ()


class IndicatorDisaggregationvalueViewSet(URFReadOnlyModelViewSet):
    serializer_class = IndicatorDisaggregationvalueSerializer
    queryset = models.IndicatorDisaggregationvalue.objects.all()


class IndicatorIndicatorblueprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatorIndicatorblueprint
        exclude = ()


class IndicatorIndicatorblueprintViewSet(URFReadOnlyModelViewSet):
    serializer_class = IndicatorIndicatorblueprintSerializer
    queryset = models.IndicatorIndicatorblueprint.objects.all()


class IndicatorIndicatorlocationdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatorIndicatorlocationdata
        exclude = ()


class IndicatorIndicatorlocationdataViewSet(URFReadOnlyModelViewSet):
    serializer_class = IndicatorIndicatorlocationdataSerializer
    queryset = models.IndicatorIndicatorlocationdata.objects.all()


class IndicatorIndicatorreportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatorIndicatorreport
        exclude = ()


class IndicatorIndicatorreportViewSet(URFReadOnlyModelViewSet):
    serializer_class = IndicatorIndicatorreportSerializer
    queryset = models.IndicatorIndicatorreport.objects.all()


class IndicatorReportableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatorReportable
        exclude = ()


class IndicatorReportableViewSet(URFReadOnlyModelViewSet):
    serializer_class = IndicatorReportableSerializer
    queryset = models.IndicatorReportable.objects.all()


class IndicatorReportableDisaggregationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatorReportableDisaggregations
        exclude = ()


class IndicatorReportableDisaggregationsViewSet(URFReadOnlyModelViewSet):
    serializer_class = IndicatorReportableDisaggregationsSerializer
    queryset = models.IndicatorReportableDisaggregations.objects.all()


class IndicatorReportablelocationgoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatorReportablelocationgoal
        exclude = ()


class IndicatorReportablelocationgoalViewSet(URFReadOnlyModelViewSet):
    serializer_class = IndicatorReportablelocationgoalSerializer
    queryset = models.IndicatorReportablelocationgoal.objects.all()


class IndicatorReportingentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatorReportingentity
        exclude = ()


class IndicatorReportingentityViewSet(URFReadOnlyModelViewSet):
    serializer_class = IndicatorReportingentitySerializer
    queryset = models.IndicatorReportingentity.objects.all()


class PartnerPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartner
        exclude = ()


class PartnerPartnerViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerSerializer
    queryset = models.PartnerPartner.objects.all()


class PartnerPartnerClustersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerClusters
        exclude = ()


class PartnerPartnerClustersViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerClustersSerializer
    queryset = models.PartnerPartnerClusters.objects.all()


class PartnerPartneractivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartneractivity
        exclude = ()


class PartnerPartneractivityViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartneractivitySerializer
    queryset = models.PartnerPartneractivity.objects.all()


class PartnerPartneractivityLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartneractivityLocations
        exclude = ()


class PartnerPartneractivityLocationsViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartneractivityLocationsSerializer
    queryset = models.PartnerPartneractivityLocations.objects.all()


class PartnerPartneractivityprojectcontextSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartneractivityprojectcontext
        exclude = ()


class PartnerPartneractivityprojectcontextViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartneractivityprojectcontextSerializer
    queryset = models.PartnerPartneractivityprojectcontext.objects.all()


class PartnerPartnerprojectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerproject
        exclude = ()


class PartnerPartnerprojectViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerprojectSerializer
    queryset = models.PartnerPartnerproject.objects.all()


class PartnerPartnerprojectAdditionalPartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerprojectAdditionalPartners
        exclude = ()


class PartnerPartnerprojectAdditionalPartnersViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerprojectAdditionalPartnersSerializer
    queryset = models.PartnerPartnerprojectAdditionalPartners.objects.all()


class PartnerPartnerprojectClustersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerprojectClusters
        exclude = ()


class PartnerPartnerprojectClustersViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerprojectClustersSerializer
    queryset = models.PartnerPartnerprojectClusters.objects.all()


class PartnerPartnerprojectLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerprojectLocations
        exclude = ()


class PartnerPartnerprojectLocationsViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerprojectLocationsSerializer
    queryset = models.PartnerPartnerprojectLocations.objects.all()


class PartnerPartnerprojectfundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerPartnerprojectfunding
        exclude = ()


class PartnerPartnerprojectfundingViewSet(URFReadOnlyModelViewSet):
    serializer_class = PartnerPartnerprojectfundingSerializer
    queryset = models.PartnerPartnerprojectfunding.objects.all()


class UnicefLowerleveloutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefLowerleveloutput
        exclude = ()


class UnicefLowerleveloutputViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefLowerleveloutputSerializer
    queryset = models.UnicefLowerleveloutput.objects.all()


class UnicefNotificationNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefNotificationNotification
        exclude = ()


class UnicefNotificationNotificationViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefNotificationNotificationSerializer
    queryset = models.UnicefNotificationNotification.objects.all()


class UnicefPdresultlinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefPdresultlink
        exclude = ()


class UnicefPdresultlinkViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefPdresultlinkSerializer
    queryset = models.UnicefPdresultlink.objects.all()


class UnicefPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefPerson
        exclude = ()


class UnicefPersonViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefPersonSerializer
    queryset = models.UnicefPerson.objects.all()


class UnicefProgrammedocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefProgrammedocument
        exclude = ()


class UnicefProgrammedocumentViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefProgrammedocumentSerializer
    queryset = models.UnicefProgrammedocument.objects.all()


class UnicefProgrammedocumentPartnerFocalPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefProgrammedocumentPartnerFocalPoint
        exclude = ()


class UnicefProgrammedocumentPartnerFocalPointViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefProgrammedocumentPartnerFocalPointSerializer
    queryset = models.UnicefProgrammedocumentPartnerFocalPoint.objects.all()


class UnicefProgrammedocumentSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefProgrammedocumentSections
        exclude = ()


class UnicefProgrammedocumentSectionsViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefProgrammedocumentSectionsSerializer
    queryset = models.UnicefProgrammedocumentSections.objects.all()


class UnicefProgrammedocumentUnicefFocalPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefProgrammedocumentUnicefFocalPoint
        exclude = ()


class UnicefProgrammedocumentUnicefFocalPointViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefProgrammedocumentUnicefFocalPointSerializer
    queryset = models.UnicefProgrammedocumentUnicefFocalPoint.objects.all()


class UnicefProgrammedocumentUnicefOfficersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefProgrammedocumentUnicefOfficers
        exclude = ()


class UnicefProgrammedocumentUnicefOfficersViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefProgrammedocumentUnicefOfficersSerializer
    queryset = models.UnicefProgrammedocumentUnicefOfficers.objects.all()


class UnicefProgressreportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefProgressreport
        exclude = ()


class UnicefProgressreportViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefProgressreportSerializer
    queryset = models.UnicefProgressreport.objects.all()


class UnicefProgressreportattachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefProgressreportattachment
        exclude = ()


class UnicefProgressreportattachmentViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefProgressreportattachmentSerializer
    queryset = models.UnicefProgressreportattachment.objects.all()


class UnicefReportingperioddatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefReportingperioddates
        exclude = ()


class UnicefReportingperioddatesViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefReportingperioddatesSerializer
    queryset = models.UnicefReportingperioddates.objects.all()


class UnicefSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnicefSection
        exclude = ()


class UnicefSectionViewSet(URFReadOnlyModelViewSet):
    serializer_class = UnicefSectionSerializer
    queryset = models.UnicefSection.objects.all()
