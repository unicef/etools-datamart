from etools_datamart.api.urls import router

from . import api

router.register(r"sources/prp/clustercluster", api.ClusterClusterViewSet)
router.register(r"sources/prp/clusterclusteractivity", api.ClusterClusteractivityViewSet)
router.register(r"sources/prp/clusterclusteractivitylocations", api.ClusterClusteractivityLocationsViewSet)
router.register(r"sources/prp/clusterclusterobjective", api.ClusterClusterobjectiveViewSet)
router.register(r"sources/prp/clusterclusterobjectivelocations", api.ClusterClusterobjectiveLocationsViewSet)
router.register(r"sources/prp/corecountry", api.CoreCountryViewSet)
router.register(r"sources/prp/corelocation", api.CoreLocationViewSet)
router.register(r"sources/prp/corelocationworkspaces", api.CoreLocationWorkspacesViewSet)
router.register(r"sources/prp/coreprprole", api.CorePrproleViewSet)
router.register(r"sources/prp/coreresponseplan", api.CoreResponseplanViewSet)
router.register(r"sources/prp/coreworkspace", api.CoreWorkspaceViewSet)
router.register(r"sources/prp/indicatordisaggregation", api.IndicatorDisaggregationViewSet)
router.register(r"sources/prp/indicatordisaggregationvalue", api.IndicatorDisaggregationvalueViewSet)
router.register(r"sources/prp/indicatorindicatorblueprint", api.IndicatorIndicatorblueprintViewSet)
router.register(r"sources/prp/indicatorindicatorlocationdata", api.IndicatorIndicatorlocationdataViewSet)
router.register(r"sources/prp/indicatorindicatorreport", api.IndicatorIndicatorreportViewSet)
router.register(r"sources/prp/indicatorreportable", api.IndicatorReportableViewSet)
router.register(r"sources/prp/indicatorreportabledisaggregations", api.IndicatorReportableDisaggregationsViewSet)
router.register(r"sources/prp/indicatorreportablelocationgoal", api.IndicatorReportablelocationgoalViewSet)
router.register(r"sources/prp/indicatorreportingentity", api.IndicatorReportingentityViewSet)
router.register(r"sources/prp/partnerpartner", api.PartnerPartnerViewSet, basename="prp_partners")
router.register(r"sources/prp/partnerpartnerclusters", api.PartnerPartnerClustersViewSet)
router.register(r"sources/prp/partnerpartneractivity", api.PartnerPartneractivityViewSet)
router.register(r"sources/prp/partnerpartneractivitylocations", api.PartnerPartneractivityLocationsViewSet)
router.register(r"sources/prp/partnerpartneractivityprojectcontext", api.PartnerPartneractivityprojectcontextViewSet)
router.register(r"sources/prp/partnerpartnerproject", api.PartnerPartnerprojectViewSet)
router.register(
    r"sources/prp/partnerpartnerprojectadditionalpartners", api.PartnerPartnerprojectAdditionalPartnersViewSet
)
router.register(r"sources/prp/partnerpartnerprojectclusters", api.PartnerPartnerprojectClustersViewSet)
router.register(r"sources/prp/partnerpartnerprojectlocations", api.PartnerPartnerprojectLocationsViewSet)
router.register(r"sources/prp/partnerpartnerprojectfunding", api.PartnerPartnerprojectfundingViewSet)
router.register(r"sources/prp/uniceffinalreview", api.UnicefFinalreviewViewSet)
router.register(
    r"sources/prp/uniceflocationscartodbtable", api.UnicefLocationsCartodbtableViewSet, basename="prp_cartodb"
)
router.register(r"sources/prp/uniceflocationsgatewaytype", api.UnicefLocationsGatewaytypeViewSet)
router.register(r"sources/prp/uniceflowerleveloutput", api.UnicefLowerleveloutputViewSet)
router.register(r"sources/prp/unicefpdresultlink", api.UnicefPdresultlinkViewSet)
router.register(r"sources/prp/unicefperson", api.UnicefPersonViewSet)
router.register(r"sources/prp/unicefprogrammedocument", api.UnicefProgrammedocumentViewSet)
router.register(
    r"sources/prp/unicefprogrammedocumentpartnerfocalpoint", api.UnicefProgrammedocumentPartnerFocalPointViewSet
)
router.register(r"sources/prp/unicefprogrammedocumentsections", api.UnicefProgrammedocumentSectionsViewSet)
router.register(
    r"sources/prp/unicefprogrammedocumentuniceffocalpoint", api.UnicefProgrammedocumentUnicefFocalPointViewSet
)
router.register(r"sources/prp/unicefprogrammedocumentunicefofficers", api.UnicefProgrammedocumentUnicefOfficersViewSet)
router.register(r"sources/prp/unicefprogressreport", api.UnicefProgressreportViewSet)
router.register(r"sources/prp/unicefprogressreportattachment", api.UnicefProgressreportattachmentViewSet)
router.register(r"sources/prp/unicefreportingperioddates", api.UnicefReportingperioddatesViewSet)
router.register(r"sources/prp/unicefsection", api.UnicefSectionViewSet)
