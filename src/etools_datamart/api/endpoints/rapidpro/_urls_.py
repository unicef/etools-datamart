from etools_datamart.api.urls import router

from . import campaign, contact, flow, flowstart, group

router.register(r"rapidpro/group", group.GroupViewSet)
router.register(r"rapidpro/contact", contact.ContactViewSet)
router.register(r"rapidpro/flow", flow.FlowViewSet)
router.register(r"rapidpro/campaign", campaign.CampaignViewSet)
router.register(r"rapidpro/flowstart", flowstart.FlowStartViewSet)
