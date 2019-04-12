from django.urls import include, path, re_path

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
# router.register(r'etools/partners/partner-organization', endpoints.PartnerViewSet, basename='partners')
router.register(r'etools/partners/plannedengagement', endpoints.PlannedengagementViewSet)
# router.register(r'etools/reports/appliedindicator', endpoints.AppliedindicatorViewSet)
router.register(r'etools/reports/results', endpoints.ReportsResultViewSet)
# router.register(r'etools/t2/ftravel', endpoints.FTravelViewSet)
# router.register(r'etools/tpm/tpmvisit', endpoints.TpmTpmvisitViewSet)

router.register(r'datamart/actionpoints', endpoints.ActionPointViewSet)
router.register(r'datamart/locations', endpoints.LocationViewSet)
router.register(r'datamart/fam-indicators', endpoints.FAMIndicatorViewSet)
router.register(r'datamart/funds-reservation', endpoints.FundsReservationViewSet)
router.register(r'datamart/hact', endpoints.HACTViewSet)
router.register(r'datamart/interventions', endpoints.InterventionViewSet)
router.register(r'datamart/interventions-locations', endpoints.InterventionByLocationViewSet)
router.register(r'datamart/pd-indicators', endpoints.PDIndicatorViewSet)
router.register(r'datamart/pmp-indicators', endpoints.PMPIndicatorsViewSet)
router.register(r'datamart/user-stats', endpoints.UserStatsViewSet)
router.register(r'datamart/users', endpoints.EtoolsUserViewSet)
router.register(r'datamart/travels', endpoints.TravelViewSet)
router.register(r'datamart/travel-activities', endpoints.TravelActivityViewSet)
router.register(r'datamart/tpm-visits', endpoints.TPMVisitViewSet)
router.register(r'datamart/tpm-activities', endpoints.TPMActivityViewSet)
router.register(r'datamart/partners', endpoints.PartnerViewSet)

router.register(r'system/monitor', endpoints.MonitorViewSet)

# urlpatterns = router.urls

urlpatterns = [
    re_path(r'(?P<version>(v1|latest))/', include(router.urls)),
    path(r'+swagger/', endpoints.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'+redoc/', endpoints.schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
