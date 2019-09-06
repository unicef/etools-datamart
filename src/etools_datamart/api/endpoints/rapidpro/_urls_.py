from etools_datamart.api.urls import router

from . import group

router.register(r'datamart/rapidpro/group', group.GroupViewSet)
