from django.urls import include, path, re_path

from unicef_rest_framework.routers import APIReadOnlyRouter

from etools_datamart.api.endpoints import schema_view

# urlpatterns = router.urls
from . import endpoints

app_name = 'api'


class ReadOnlyRouter(APIReadOnlyRouter):
    pass


router = ReadOnlyRouter()
router.register(r'sources/etools/funds/fundsreservationheader', endpoints.EtoolsFundsReservationHeaderViewSet)
router.register(r'sources/etools/funds/fundsreservationitem', endpoints.EtoolsFundsreservationitemViewSet)
router.register(r'sources/etools/funds/grant', endpoints.EtoolsGrantViewSet)
router.register(r'sources/etools/partners/assessment', endpoints.EtoolsAssessmentViewSet)
router.register(r'sources/etools/partners/plannedengagement', endpoints.EtoolsPlannedengagementViewSet)
router.register(r'sources/etools/workspaces', endpoints.EtoolsWorkspaceViewSet)

router.register(r'datamart/attachment/attachment', endpoints.AttachmentViewSet)
router.register(r'datamart/funds/grants', endpoints.GrantViewSet)
router.register(r'datamart/audit/audit', endpoints.AuditViewSet)
router.register(r'datamart/audit/engagements', endpoints.EngagementViewSet)
router.register(r'datamart/audit/engagement-details', endpoints.EngagementDetailViewSet, basename="engagement-details")
router.register(r'datamart/audit/micro-assessment', endpoints.MicroAssessmentViewSet)
router.register(r'datamart/audit/results', endpoints.AuditResultViewSet)
router.register(r'datamart/audit/special-audit', endpoints.AuditSpecialViewSet)
router.register(r'datamart/audit/spot-check-findings', endpoints.SpotCheckFindingViewSet)
router.register(r'datamart/actionpoints', endpoints.ActionPointViewSet)
router.register(r'datamart/locations', endpoints.LocationViewSet)
router.register(r'datamart/location-sites', endpoints.LocationSiteViewSet)
router.register(r'datamart/gateway-type', endpoints.GatewayTypeViewSet)
router.register(r'datamart/office', endpoints.OfficeViewSet)
router.register(r'datamart/fam-indicators', endpoints.FAMIndicatorViewSet)
router.register(r'datamart/fm-questions', endpoints.FMQuestionViewSet)
router.register(r'datamart/fm-ontrack', endpoints.FMOntrackViewSet)
router.register(r'datamart/fm-options', endpoints.FMOptionsViewSet)
router.register(r'datamart/funds-reservation', endpoints.FundsReservationViewSet)
router.register(r'datamart/hact/aggregate', endpoints.HACTAggreagateViewSet)
router.register(r'datamart/hact/history', endpoints.HACTHistoryViewSet)
router.register(r'datamart/interventions', endpoints.InterventionViewSet)
router.register(r'datamart/interventions-locations', endpoints.InterventionByLocationViewSet)
router.register(r'datamart/interventions-budget', endpoints.InterventionBudgetViewSet)
router.register(r'datamart/pd-indicators', endpoints.PDIndicatorViewSet)
router.register(r'datamart/pmp-indicators', endpoints.PMPIndicatorsViewSet)
router.register(r'datamart/user-stats', endpoints.UserStatsViewSet)

router.register(r'datamart/partners/contacts', endpoints.PartnerStaffMemberViewSet)
router.register(r'datamart/partners/agreements', endpoints.PartnerAgreementViewSet)

router.register(r'datamart/psea/assessments', endpoints.PseaAssessmentViewSet)
router.register(r'datamart/psea/answers', endpoints.PseaAnswerViewSet)

router.register(r'datamart/reports/sections', endpoints.SectionViewSet)
router.register(r'datamart/reports/indicators', endpoints.IndicatorViewSet)

router.register(r'datamart/reports/outcomes', endpoints.OutcomeViewSet, basename='outcome')
router.register(r'datamart/reports/outputs', endpoints.OutputViewSet, basename='output')
router.register(r'datamart/reports/activities', endpoints.ActivityViewSet, basename='activity')

router.register(r'datamart/users', endpoints.EtoolsUserViewSet)
router.register(r'datamart/travels', endpoints.TravelViewSet)
router.register(r'datamart/travel-activities', endpoints.TravelActivityViewSet)
router.register(r'datamart/t2f/trips', endpoints.TripViewSet)
router.register(r'datamart/tpm-visits', endpoints.TPMVisitViewSet)
router.register(r'datamart/tpm-activities', endpoints.TPMActivityViewSet)
router.register(r'datamart/partners', endpoints.PartnerViewSet)

router.register(r'prp/datareport', endpoints.DataReportViewSet)

router.register(r'system/monitor', endpoints.MonitorViewSet)

from etools_datamart.apps.sources.source_prp import api_urls  # noqa isort:skip
from etools_datamart.apps.sources.source_prp.backward_api_urls import backward_compatible_router  # noqa isort:skip

from .endpoints.rapidpro import _urls_  # noqa isort:skip

urlpatterns = [
    re_path(r'(?P<version>(v1|v2|latest))/', include(router.urls)),
    re_path(r'(?P<version>(v1|v2|latest))/', include(backward_compatible_router.urls)),

    re_path(r'\+sw(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
            name='schema-json'),

    path(r'+swagger/', endpoints.schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path(r'+redoc/', endpoints.schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
