from unicef_rest_framework.routers import APIReadOnlyRouter

from . import api

app_name = "backward_compatible_prp"


class BackwardCompatibleRouter(APIReadOnlyRouter):
    def get_default_basename(self, viewset):
        """
        If `basename` is not specified, attempt to automatically determine
        it from the viewset.
        """
        queryset = getattr(viewset, "queryset", None)

        assert queryset is not None, (
            "`basename` argument not specified, and could "
            "not automatically determine the name from the viewset, as "
            "it does not have a `.queryset` attribute."
        )

        return "backward-" + queryset.model._meta.object_name.lower()


backward_compatible_router = BackwardCompatibleRouter()

backward_compatible_router.register(r"prp/clustercluster", api.ClusterClusterViewSet)
backward_compatible_router.register(r"prp/clusterclusteractivity", api.ClusterClusteractivityViewSet)
backward_compatible_router.register(r"prp/clusterclusteractivitylocations", api.ClusterClusteractivityLocationsViewSet)
backward_compatible_router.register(r"prp/clusterclusterobjective", api.ClusterClusterobjectiveViewSet)
backward_compatible_router.register(
    r"prp/clusterclusterobjectivelocations", api.ClusterClusterobjectiveLocationsViewSet
)
backward_compatible_router.register(r"prp/corecartodbtable", api.UnicefLocationsCartodbtableViewSet)
backward_compatible_router.register(r"sources/prp/corecartodbtable", api.UnicefLocationsCartodbtableViewSet)
backward_compatible_router.register(r"prp/corecountry", api.CoreCountryViewSet)
backward_compatible_router.register(r"prp/coregatewaytype", api.UnicefLocationsGatewaytypeViewSet)
backward_compatible_router.register(r"sources/prp/coregatewaytype", api.UnicefLocationsGatewaytypeViewSet)
backward_compatible_router.register(r"prp/corelocation", api.CoreLocationViewSet)
backward_compatible_router.register(r"prp/coreprprole", api.CorePrproleViewSet)
backward_compatible_router.register(r"prp/coreresponseplan", api.CoreResponseplanViewSet)
backward_compatible_router.register(r"prp/coreworkspace", api.CoreWorkspaceViewSet)
backward_compatible_router.register(r"prp/indicatordisaggregation", api.IndicatorDisaggregationViewSet)
backward_compatible_router.register(r"prp/indicatordisaggregationvalue", api.IndicatorDisaggregationvalueViewSet)
backward_compatible_router.register(r"prp/indicatorindicatorblueprint", api.IndicatorIndicatorblueprintViewSet)
backward_compatible_router.register(r"prp/indicatorindicatorlocationdata", api.IndicatorIndicatorlocationdataViewSet)
backward_compatible_router.register(r"prp/indicatorindicatorreport", api.IndicatorIndicatorreportViewSet)
backward_compatible_router.register(r"prp/indicatorreportable", api.IndicatorReportableViewSet)
backward_compatible_router.register(
    r"prp/indicatorreportabledisaggregations", api.IndicatorReportableDisaggregationsViewSet
)
backward_compatible_router.register(r"prp/indicatorreportablelocationgoal", api.IndicatorReportablelocationgoalViewSet)
backward_compatible_router.register(r"prp/indicatorreportingentity", api.IndicatorReportingentityViewSet)
backward_compatible_router.register(r"prp/partnerpartner", api.PartnerPartnerViewSet)
backward_compatible_router.register(r"prp/partnerpartnerclusters", api.PartnerPartnerClustersViewSet)
backward_compatible_router.register(r"prp/partnerpartneractivity", api.PartnerPartneractivityViewSet)
backward_compatible_router.register(r"prp/partnerpartneractivitylocations", api.PartnerPartneractivityLocationsViewSet)
backward_compatible_router.register(
    r"prp/partnerpartneractivityprojectcontext", api.PartnerPartneractivityprojectcontextViewSet
)
backward_compatible_router.register(r"prp/partnerpartnerproject", api.PartnerPartnerprojectViewSet)
backward_compatible_router.register(
    r"prp/partnerpartnerprojectadditionalpartners", api.PartnerPartnerprojectAdditionalPartnersViewSet
)
backward_compatible_router.register(r"prp/partnerpartnerprojectclusters", api.PartnerPartnerprojectClustersViewSet)
backward_compatible_router.register(r"prp/partnerpartnerprojectlocations", api.PartnerPartnerprojectLocationsViewSet)
backward_compatible_router.register(r"prp/partnerpartnerprojectfunding", api.PartnerPartnerprojectfundingViewSet)
backward_compatible_router.register(r"prp/uniceflowerleveloutput", api.UnicefLowerleveloutputViewSet)
backward_compatible_router.register(r"prp/unicefpdresultlink", api.UnicefPdresultlinkViewSet)
backward_compatible_router.register(r"prp/unicefperson", api.UnicefPersonViewSet)
backward_compatible_router.register(r"prp/unicefprogrammedocument", api.UnicefProgrammedocumentViewSet)
backward_compatible_router.register(
    r"prp/unicefprogrammedocumentpartnerfocalpoint", api.UnicefProgrammedocumentPartnerFocalPointViewSet
)
backward_compatible_router.register(r"prp/unicefprogrammedocumentsections", api.UnicefProgrammedocumentSectionsViewSet)
backward_compatible_router.register(
    r"prp/unicefprogrammedocumentuniceffocalpoint", api.UnicefProgrammedocumentUnicefFocalPointViewSet
)
backward_compatible_router.register(
    r"prp/unicefprogrammedocumentunicefofficers", api.UnicefProgrammedocumentUnicefOfficersViewSet
)
backward_compatible_router.register(r"prp/unicefprogressreport", api.UnicefProgressreportViewSet)
backward_compatible_router.register(r"prp/unicefprogressreportattachment", api.UnicefProgressreportattachmentViewSet)
backward_compatible_router.register(r"prp/unicefreportingperioddates", api.UnicefReportingperioddatesViewSet)
backward_compatible_router.register(r"prp/unicefsection", api.UnicefSectionViewSet)
