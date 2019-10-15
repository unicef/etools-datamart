from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from etools_datamart.apps.data.loader import EtoolsLoader
from etools_datamart.apps.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.data.models.mixins import add_location_mapping, LocationMixin
from etools_datamart.apps.etools.enrichment.consts import (ActionPointConsts, AuditEngagementConsts,
                                                           CategoryConsts, PartnersInterventionConst,)
from etools_datamart.apps.etools.models import (ActionPointsActionpoint, AuditAudit, AuditMicroassessment,
                                                AuditSpecialaudit, AuditSpotcheck, DjangoComments,
                                                DjangoContentType, T2FTravelactivity, TpmTpmactivity,)

from .intervention import Intervention

# reference_number(self):
# return '{}/{}/{}/APD'.format(
#     connection.tenant.country_short_code or '',
#     self.created.year,
#     self.id,
# )
ENGAGEMENTS = [AuditSpotcheck, AuditMicroassessment, AuditSpecialaudit, AuditAudit]
ENGAGEMENTS_NAMES = [c.__name__ for c in ENGAGEMENTS]

RELATED_MODULES = ENGAGEMENTS + [TpmTpmactivity, T2FTravelactivity]

RELATED_MODULE_NAMES = [c.__name__ for c in RELATED_MODULES]
RELATED_MODULE_CHOICES = zip(RELATED_MODULE_NAMES, RELATED_MODULE_NAMES)


class ActionPointLoader(EtoolsLoader):

    def get_reference_number(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        country = self.context['country']
        return '{}/{}/{}/APD'.format(country.country_short_code or '',
                                     record.created.year,
                                     record.id)

    # def get_category_module(self, original: ActionPointsActionpoint, values: dict):
    #     if original.engagement:
    #         return original.engagement.engagement_type

    def get_actions_taken(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        ct = DjangoContentType.objects.get(app_label='action_points', model='actionpoint')
        comments = DjangoComments.objects.filter(object_pk=record.id,
                                                 content_type=ct)
        return ";\n\n".join(["{} ({}): {}".format(c.user if c.user else '-', c.submit_date.strftime(
            "%d %b %Y"), c.comment) for c in comments.all()])

    # def get_module_task_activity_reference_number(self, original: ActionPointsActionpoint, values: dict):
    #     if original.tpm_activity:
    #         return original.tpm_activity.tpm_visit.reference_number
    #
    def get_related_module_id(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        module = values['related_module_class']
        if module in ENGAGEMENTS_NAMES:
            return record.engagement.pk
        elif module == 'TpmTpmactivity':
            return record.tpm_activity.tpm_visit_id
        elif module == 'T2FTravelactivity':
            return record.travel_activity.pk
        elif module is None:
            return None
        raise ValueError(values['related_module_class'])

    def get_related_module_class(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        if record.engagement:
            for target in ENGAGEMENTS:
                try:
                    target.objects.get(engagement_ptr=record.engagement_id)
                    return target.__name__
                except ObjectDoesNotExist:
                    pass
            return 'Error'
        elif record.tpm_activity:
            return 'TpmTpmactivity'
        elif record.travel_activity:
            return 'T2FTravelactivity'
        return None

    def get_engagement_subclass(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        # targets = [AuditSpotcheck, AuditMicroassessment, AuditSpecialaudit, AuditAudit]
        if not record.engagement:
            return None
        for target in ENGAGEMENTS:
            try:
                target.objects.get(engagement_ptr=record.engagement_id)
                return target.__name__
            except ObjectDoesNotExist:
                pass
        raise ValueError('Cannot find subclass for ActionPoint #%s Engagement %s' % (record.id,
                                                                                     record.engagement_id))

    def get_intervention_number(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        intervention = record.intervention
        if intervention:
            agreement_base_number = intervention.agreement.agreement_number.split('-')[0]
            if intervention.document_type != PartnersInterventionConst.SSFA:
                number = '{agreement}/{type}{year}{id}'.format(
                    agreement=agreement_base_number,
                    type=intervention.document_type,
                    year=intervention.reference_number_year,
                    id=intervention.id
                )
                return number
            return agreement_base_number

    def get_module_reference_number(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        if record.engagement:
            engagement_code = 'a' if record.engagement.engagement_type == AuditEngagementConsts.TYPE_AUDIT else record.engagement.engagement_type
            return '{}/{}/{}/{}/{}'.format(
                self.context['country'].country_short_code or '',
                record.partner.name[:5],
                engagement_code.upper(),
                record.created.year,
                record.id
            )
        elif record.tpm_activity:
            return record.tpm_activity.tpm_visit.reference_number
        elif record.travel_activity:
            ta = record.travel_activity
            travel = ta.travels.filter(traveler=ta.primary_traveler).first()
            if not travel:
                return
            return travel.reference_number

    def get_module_task_activity_reference_number(self, record: ActionPointsActionpoint, values: dict, **kwargs):
        obj = record.related_object
        if not obj:
            return 'n/a'

        if record.tpm_activity:
            return obj.tpm_visit.reference_number


class ActionPoint(LocationMixin, EtoolsDataMartModel):
    reference_number = models.CharField(max_length=200, blank=True, null=True, db_index=True)

    author_username = models.CharField(max_length=200, blank=True, null=True)
    assigned_by_name = models.CharField(max_length=200, blank=True, null=True)
    assigned_by_email = models.CharField(max_length=200, blank=True, null=True)
    assigned_to_name = models.CharField(max_length=200, blank=True, null=True)
    assigned_to_email = models.CharField(max_length=200, blank=True, null=True)

    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10,
                              choices=ActionPointConsts.STATUSES,
                              blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    date_of_completion = models.DateTimeField(blank=True, null=True)
    high_priority = models.BooleanField(blank=True, null=True, db_index=True)
    cp_output = models.TextField(blank=True, null=True)
    cp_output_id = models.IntegerField(blank=True, null=True)

    # Intervention
    intervention_source_id = models.IntegerField(blank=True, null=True)
    intervention_number = models.CharField(max_length=64, blank=True, null=True)
    intervention_title = models.CharField(max_length=256, blank=True, null=True)

    office = models.CharField(max_length=64, blank=True, null=True)

    partner_source_id = models.IntegerField(blank=True, null=True)
    partner_name = models.CharField(max_length=300, blank=True, null=True)
    vendor_number = models.CharField(max_length=30, blank=True, null=True)

    engagement_source_id = models.IntegerField(blank=True, null=True)
    engagement_type = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    engagement_subclass = models.CharField(max_length=64, blank=True, null=True, db_index=True)

    related_module_class = models.CharField(max_length=64,
                                            choices=RELATED_MODULE_CHOICES,
                                            blank=True, null=True, db_index=True)
    related_module_id = models.IntegerField(blank=True, null=True, db_index=True)
    section_source_id = models.IntegerField(blank=True, null=True)
    section_type = models.CharField(max_length=64, blank=True, null=True)

    # tpm_activity_source_id = models.IntegerField()
    # tpm_activity = models.CharField(max_length=64, null=True)
    tpm_activity_source_id = models.IntegerField(blank=True, null=True)

    travel_activity_source_id = models.IntegerField(blank=True, null=True)
    travel_activity_travel_type = models.CharField(max_length=64, blank=True, null=True)

    category_source_id = models.IntegerField(blank=True, null=True)
    category_module = models.CharField(max_length=64,
                                       choices=CategoryConsts.MODULE_CHOICES,
                                       blank=True, null=True)
    category_description = models.CharField(max_length=300, blank=True, null=True)

    actions_taken = models.TextField(blank=True, null=True)
    module_reference_number = models.CharField(max_length=300, blank=True, null=True)
    module_task_activity_reference_number = models.CharField(max_length=300, blank=True, null=True)
    # related_module_url = models.CharField(max_length=300, blank=True, null=True)
    # action_point_url = models.CharField(max_length=300, blank=True, null=True)

    loader = ActionPointLoader()

    class Options:
        source = ActionPointsActionpoint
        depends = (Intervention,)
        mapping = add_location_mapping(dict(
            assigned_by_name='assigned_by.get_display_name',
            assigned_by_email='assigned_by.email',
            assigned_to_name='assigned_to.get_display_name',
            assigned_to_email='assigned_to.email',
            author_username='author.username',
            category_description='category.description',
            category_module='category.module',
            category_source_id='category.id',
            cp_output='cp_output.name',
            cp_output_id='cp_output.id',
            engagement_source_id='engagement.id',
            engagement_type='engagement.engagement_type',
            intervention_source_id='intervention.id',
            intervention_title='intervention.title',
            office='office.name',
            partner_name='partner.name',
            partner_source_id='partner.id',
            section_source_id='section.id',
            section_type='section.name',
            tpm_activity_source_id='tpm_activity.id',
            travel_activity_source_id='travel_activity.id',
            travel_activity_travel_type='travel_activity.travel_type',
            vendor_number='partner.vendor_number',

        ))
