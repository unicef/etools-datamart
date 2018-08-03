from django.conf.urls import url
from rest_framework import routers
from rest_framework.routers import Route, DynamicRoute

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
        """
        Generate the list of URL patterns, including a default root view
        for the API, and appending `.json` style format suffixes.
        """
        urls = super(ReadOnlyRouter, self).get_urls()

        if self.include_root_view:
            view = self.get_api_root_view(api_urls=urls)
            root_url = url(r'^$', view, name=self.root_view_name)
            urls.append(root_url)

        return urls


router = ReadOnlyRouter()
router.register(r'partners', views.PartnerViewSet, base_name='partners')
router.register(r'results', views.ReportsResultViewSet)

urlpatterns = router.urls
