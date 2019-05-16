from django.urls import include, path, re_path

from unicef_rest_framework.routers import APIReadOnlyRouter

from . import endpoints

app_name = 'api'


class ReadOnlyRouter(APIReadOnlyRouter):
    pass


v1 = ReadOnlyRouter()
v1.register(r'etools/audit/engagement', endpoints.EngagementViewSet)
v1.register(r'etools/funds/fundsreservationheader', endpoints.FundsReservationHeaderViewSet)
v1.register(r'etools/funds/fundsreservationitem', endpoints.FundsreservationitemViewSet)
v1.register(r'etools/funds/grant', endpoints.GrantViewSet)
v1.register(r'etools/partners/agreement', endpoints.AgreementViewSet)
v1.register(r'etools/partners/assessment', endpoints.AssessmentViewSet)
v1.register(r'etools/partners/plannedengagement', endpoints.PlannedengagementViewSet)
v1.register(r'datamart/actionpoints', endpoints.ActionPointViewSet)
v1.register(r'datamart/locations', endpoints.LocationViewSet)
v1.register(r'datamart/fam-indicators', endpoints.FAMIndicatorViewSet)
v1.register(r'datamart/funds-reservation', endpoints.FundsReservationViewSet)
v1.register(r'datamart/hact', endpoints.HACTViewSet)
v1.register(r'datamart/interventions', endpoints.InterventionViewSet)
v1.register(r'datamart/interventions-locations', endpoints.InterventionByLocationViewSet)
v1.register(r'datamart/interventions-budget', endpoints.InterventionBudgetViewSet)
v1.register(r'datamart/pd-indicators', endpoints.PDIndicatorViewSet)
v1.register(r'datamart/pmp-indicators', endpoints.PMPIndicatorsViewSet)
v1.register(r'datamart/user-stats', endpoints.UserStatsViewSet)

v1.register(r'datamart/reports/sections', endpoints.SectionViewSet)

v1.register(r'datamart/users', endpoints.EtoolsUserViewSet)
v1.register(r'datamart/user-offices', endpoints.OfficeViewSet)
v1.register(r'datamart/travels', endpoints.TravelViewSet)
v1.register(r'datamart/travel-activities', endpoints.TravelActivityViewSet)
v1.register(r'datamart/tpm-visits', endpoints.TPMVisitViewSet)
v1.register(r'datamart/tpm-activities', endpoints.TPMActivityViewSet)
v1.register(r'datamart/partners', endpoints.PartnerViewSet)

v1.register(r'system/monitor', endpoints.MonitorViewSet)

v2 = ReadOnlyRouter()
v2.register(r'etools/audit/engagement', endpoints.EngagementViewSet)


urlpatterns = [
    re_path(r'(?P<version>(v1))/', include(v1.urls)),
    re_path(r'(?P<version>(v2|latest))/', include(v2.urls)),

    path(r'+swagger/', endpoints.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'+redoc/', endpoints.schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
