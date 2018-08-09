from django.conf.urls import url
from rest_framework import routers
from rest_framework.routers import DynamicRoute, Route

from . import views

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
router.register(r'partners/partner-organization', views.PartnerViewSet, base_name='partners')
router.register(r'reports/results', views.ReportsResultViewSet)
router.register(r'funds/grant', views.GrantViewSet)
router.register(r'partners/assessment', views.AssessmentViewSet)
router.register(r'partners/agreement', views.AgreementViewSet)
router.register(r'audit/engagement', views.EngagementViewSet)
router.register(r'partners/intervention', views.InterventionViewSet)
router.register(r't2/ftravel', views.FTravelViewSet)
router.register(r'reports/appliedindicator', views.AppliedindicatorViewSet)
router.register(r'funds/fundsreservationitem', views.FundsreservationitemViewSet)
router.register(r'funds/fundsreservationheader', views.FundsReservationHeaderViewSet)
router.register(r'partners/plannedengagement', views.PlannedengagementViewSet)
router.register(r'partners/plannedengagement', views.PlannedengagementViewSet)
router.register(r'partners/plannedengagement', views.PlannedengagementViewSet)

urlpatterns = router.urls
