from django.conf.urls import url
from unicef_rest_framework.routers import APIReadOnlyRouter

from . import endpoints

app_name = 'api'


class ReadOnlyRouter(APIReadOnlyRouter):
    pass


router = ReadOnlyRouter()
router.register(r'audit/engagement', endpoints.EngagementViewSet)
router.register(r'funds/fundsreservationheader', endpoints.FundsReservationHeaderViewSet)
router.register(r'funds/fundsreservationitem', endpoints.FundsreservationitemViewSet)
router.register(r'funds/grant', endpoints.GrantViewSet)
router.register(r'partners/agreement', endpoints.AgreementViewSet)
router.register(r'partners/assessment', endpoints.AssessmentViewSet)
router.register(r'partners/intervention', endpoints.InterventionViewSet)
router.register(r'partners/partner-organization', endpoints.PartnerViewSet, base_name='partners')
router.register(r'partners/plannedengagement', endpoints.PlannedengagementViewSet)
router.register(r'partners/plannedengagement', endpoints.PlannedengagementViewSet)
router.register(r'partners/plannedengagement', endpoints.PlannedengagementViewSet)
router.register(r'reports/appliedindicator', endpoints.AppliedindicatorViewSet)
router.register(r'reports/results', endpoints.ReportsResultViewSet)
router.register(r't2/ftravel', endpoints.FTravelViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', endpoints.schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', endpoints.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', endpoints.schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
