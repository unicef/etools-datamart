from rest_framework import routers
from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'partners', views.PartnerViewSet, base_name='partners')
router.register(r'results', views.ReportsResultViewSet)

urlpatterns = router.urls
