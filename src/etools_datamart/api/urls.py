from django.conf.urls import url
from rest_framework import routers
from rest_framework.routers import DynamicRoute, Route

from . import endpoints

app_name = 'api'


class ReadOnlyRouter(routers.DefaultRouter):
    include_format_suffixes = False
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]

    def get_urls(self):
        urls = super(ReadOnlyRouter, self).get_urls()
        view = self.get_api_root_view(api_urls=urls)
        root_url = url(r'^$', view, name=self.root_view_name)
        urls.append(root_url)
        return urls


router = ReadOnlyRouter()
router.register(r'partners/partner-organization', endpoints.PartnerViewSet, base_name='partners')
router.register(r'reports/results', endpoints.ReportsResultViewSet)
router.register(r'funds/grant', endpoints.GrantViewSet)
router.register(r'partners/assessment', endpoints.AssessmentViewSet)
router.register(r'partners/agreement', endpoints.AgreementViewSet)
router.register(r'audit/engagement', endpoints.EngagementViewSet)
router.register(r'partners/intervention', endpoints.InterventionViewSet)
router.register(r't2/ftravel', endpoints.FTravelViewSet)
router.register(r'reports/appliedindicator', endpoints.AppliedindicatorViewSet)
router.register(r'funds/fundsreservationitem', endpoints.FundsreservationitemViewSet)
router.register(r'funds/fundsreservationheader', endpoints.FundsReservationHeaderViewSet)
router.register(r'partners/plannedengagement', endpoints.PlannedengagementViewSet)
router.register(r'partners/plannedengagement', endpoints.PlannedengagementViewSet)
router.register(r'partners/plannedengagement', endpoints.PlannedengagementViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', endpoints.schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', endpoints.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', endpoints.schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
