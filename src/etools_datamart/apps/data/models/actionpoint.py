from django.db import models
from django.utils.functional import cached_property

from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.data.models.mixins import add_location_mapping, LocationMixin
from etools_datamart.apps.etools.enrichment.consts import ActionPointConsts, CategoryConsts
from etools_datamart.apps.etools.models import ActionPointsActionpoint, DjangoComments, DjangoContentType, \
    PartnersIntervention, AuditEngagement, AuditSpotcheck, AuditMicroassessment, AuditAudit, AuditSpecialaudit


# reference_number(self):
# return '{}/{}/{}/APD'.format(
#     connection.tenant.country_short_code or '',
#     self.created.year,
#     self.id,
# )


class ActionPointLoader(Loader):

    def get_reference_number(self, original: ActionPointsActionpoint, values: dict):
        country = self.context['country']
        return '{}/{}/{}/APD'.format(country.country_short_code or '',
                                     original.created.year,
                                     original.id)

    # def get_category_module(self, original: ActionPointsActionpoint, values: dict):
    #     if original.engagement:
    #         return original.engagement.engagement_type

    def get_actions_taken(self, original: ActionPointsActionpoint, values: dict):
        ct = DjangoContentType.objects.get(app_label='action_points', model='actionpoint')
        comments = DjangoComments.objects.filter(object_pk=original.id,
                                                 content_type=ct)
        return ";\n\n".join(["{} ({}): {}".format(c.user if c.user else '-', c.submit_date.strftime(
            "%d %b %Y"), c.comment) for c in comments.all()])

    def get_intervention_number(self, original: ActionPointsActionpoint, values: dict):
        intervention = original.intervention
        if intervention:
            agreement_base_number = intervention.agreement.agreement_number.split('-')[0]
            if intervention.document_type != PartnersIntervention.SSFA:
                number = '{agreement}/{type}{year}{id}'.format(
                    agreement=agreement_base_number,
                    type=intervention.document_type,
                    year=intervention.reference_number_year,
                    id=intervention.id
                )
                return number
            return agreement_base_number

    def get_module_reference_number(self, original: ActionPointsActionpoint, values: dict):
        if original.engagement:
            engagement_code = 'a' if original.engagement.engagement_type == AuditEngagement.TYPE_AUDIT else original.engagement.engagement_type
            return '{}/{}/{}/{}/{}'.format(
                self.context['country'].country_short_code or '',
                original.partner.name[:5],
                engagement_code.upper(),
                original.created.year,
                original.id
            )
        elif original.tpm_activity:
            return original.tpm_activity.tpm_visit.get_reference_number(self.context['country'])
        elif original.travel_activity:
            ta = original.travel_activity
            travel = ta.travels.filter(traveler=ta.primary_traveler).first()
            if not travel:
                return
            return travel.reference_number

    def get_module_task_activity_reference_number(self, original: ActionPointsActionpoint, values: dict):
        obj = original.related_object
        if not obj:
            return 'n/a'

        # if original.tpm_activity:
        #     return 'Task No {0} for Visit {1}'.format(obj.task_number, obj.tpm_visit.reference_number)


class ActionPoint(LocationMixin, DataMartModel):
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
    related_module_url = models.CharField(max_length=300, blank=True, null=True)
    action_point_url = models.CharField(max_length=300, blank=True, null=True)


    loader = ActionPointLoader()

    class Options:
        source = ActionPointsActionpoint
        mapping = add_location_mapping(dict(
            assigned_by_name='assigned_by.get_display_name',
            assigned_to_name='assigned_to.get_display_name',
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
