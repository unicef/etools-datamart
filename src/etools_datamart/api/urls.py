from django.conf.urls import url
from unicef_rest_framework.routers import APIReadOnlyRouter

from . import endpoints

app_name = 'api'


class ReadOnlyRouter(APIReadOnlyRouter):
    pass


router = ReadOnlyRouter()
router.register(r'etools/audit/engagement', endpoints.EngagementViewSet)
router.register(r'etools/funds/fundsreservationheader', endpoints.FundsReservationHeaderViewSet)
router.register(r'etools/funds/fundsreservationitem', endpoints.FundsreservationitemViewSet)
router.register(r'etools/funds/grant', endpoints.GrantViewSet)
router.register(r'etools/partners/agreement', endpoints.AgreementViewSet)
router.register(r'etools/partners/assessment', endpoints.AssessmentViewSet)
router.register(r'etools/partners/partner-organization', endpoints.PartnerViewSet, base_name='partners')
router.register(r'etools/partners/plannedengagement', endpoints.PlannedengagementViewSet)
router.register(r'etools/partners/plannedengagement', endpoints.PlannedengagementViewSet)
router.register(r'etools/partners/plannedengagement', endpoints.PlannedengagementViewSet)
router.register(r'etools/reports/appliedindicator', endpoints.AppliedindicatorViewSet)
router.register(r'etools/reports/results', endpoints.ReportsResultViewSet)
router.register(r'etools/t2/ftravel', endpoints.FTravelViewSet)

router.register(r'datamart/pmp-indicators', endpoints.PMPIndicatorsViewSet)
router.register(r'datamart/interventions', endpoints.InterventionViewSet)

router.register(r'system/tasks-log', endpoints.TaskLogViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', endpoints.schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', endpoints.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', endpoints.schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
