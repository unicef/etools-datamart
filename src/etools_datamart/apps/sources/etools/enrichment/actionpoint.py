import logging

from django.core.exceptions import ObjectDoesNotExist

from etools_datamart.apps.sources.etools.models import (
    ActionPointsActionpoint,
    AuditAudit,
    AuditMicroassessment,
    AuditSpecialaudit,
    AuditSpotcheck,
)

logger = logging.getLogger()


# ActionPointsActionpoint.MODULE_CHOICES = Choices(
#     ('apd', 'Action Points'),
#     ('t2f', 'Trip Management'),
#     ('tpm', 'Third Party Monitoring'),
#     ('audit', 'Financial Assurance'),
# )
#
# ActionPointsActionpoint.MAPS = {AuditEngagementConsts.TYPE_SPOT_CHECK: AuditSpotcheck,
#                                 AuditEngagementConsts.TYPE_AUDIT: AuditMicroassessment,
#                                 AuditEngagementConsts.TYPE_MICRO_ASSESSMENT: AuditAudit,
#                                 AuditEngagementConsts.TYPE_SPECIAL_AUDIT: AuditSpecialaudit,
#                                 }


def get_related_object(self):
    targets = [AuditSpotcheck, AuditMicroassessment, AuditSpecialaudit, AuditAudit]
    if self.engagement:
        for target in targets:
            try:
                return target.objects.get(engagement_ptr=self.engagement_id)
            except ObjectDoesNotExist:
                pass
                # logger.error("Cannot retrieve related for ActionPoint #%s in %s" % (
                #     self.pk,
                #     self.schema))
    # if self.engagement:
    #     obj = None
    #     try:
    #         model_name = self.MAPS[self.engagement.engagement_type]
    #         model = import_string('etools_datamart.apps.etools.models.%s' % model_name)
    #         obj = model.objects.get(engagement_ptr=self.engagement_id)
    #     except ObjectDoesNotExist as e:
    #         capture_exception()
    #         logger.error("Cannot retrieve related object %s "
    #                      "'%s' for ActionPoint #%s in %s" % (model.__name__,
    #                                                          self.engagement.engagement_type,
    #                                                          self.pk,
    #                                                          self.schema))
    #     return obj
    elif self.tpm_activity:
        return self.tpm_activity
    elif self.travel_activity:
        return self.travel_activity


def get_related_module(self):
    if self.engagement:
        return self.MODULE_CHOICES.audit
    if self.tpm_activity:
        return self.MODULE_CHOICES.tpm
    if self.travel_activity:
        return self.MODULE_CHOICES.t2f
    return self.MODULE_CHOICES.apd


def get_reference_number(self, country):
    return '{}/{}/{}/APD'.format(
        country.country_short_code or '',
        self.created.year,
        self.id,
    )


ActionPointsActionpoint.related_object = property(get_related_object)
ActionPointsActionpoint.related_module = property(get_related_module)
ActionPointsActionpoint.get_reference_number = get_reference_number
