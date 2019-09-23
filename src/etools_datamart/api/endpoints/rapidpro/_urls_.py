from etools_datamart.api.urls import router

from . import contact, group

router.register(r'rapidpro/group', group.GroupViewSet)
router.register(r'rapidpro/contact', contact.ContactViewSet)
