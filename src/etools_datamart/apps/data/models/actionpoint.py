from django.db import models

from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.data.models.mixins import add_location_mapping, LocationMixin
from etools_datamart.apps.etools.enrichment.consts import ActionPointConsts, CategoryConsts
from etools_datamart.apps.etools.models import ActionPointsActionpoint


class ActionPoint(LocationMixin, DataMartModel):
    author_username = models.CharField(max_length=200)
    assigned_by_username = models.CharField(max_length=200)
    assigned_to_username = models.CharField(max_length=200)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10,
                              choices=ActionPointConsts.STATUSES,
                              blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    date_of_completion = models.DateTimeField(blank=True, null=True)
    high_priority = models.BooleanField(blank=True, null=True)

    # Intervention
    intervention_source_id = models.IntegerField(blank=True, null=True)
    intervention_number = models.CharField(max_length=64, null=True)

    office = models.CharField(max_length=64, blank=True, null=True)

    partner_source_id = models.IntegerField(blank=True, null=True)
    partner_name = models.CharField(max_length=300, blank=True, null=True)

    engagement_source_id = models.IntegerField(blank=True, null=True)
    engagement_type = models.CharField(max_length=64, blank=True, null=True)

    section_source_id = models.IntegerField(blank=True, null=True)
    section_type = models.CharField(max_length=64, blank=True, null=True)

    # tpm_activity_source_id = models.IntegerField()
    # tpm_activity = models.CharField(max_length=64, null=True)

    travel_activity_source_id = models.IntegerField(blank=True, null=True)
    travel_activity_travel_type = models.CharField(max_length=64, blank=True, null=True)

    category_source_id = models.IntegerField(blank=True, null=True)
    category_module = models.CharField(max_length=64,
                                       choices=CategoryConsts.MODULE_CHOICES,
                                       blank=True, null=True)

    # assigned_by = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='authuser_action_points_actionpoint_assigned_by_id')
    # assigned_to = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='authuser_action_points_actionpoint_assigned_to_id')
    # author = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='authuser_action_points_actionpoint_author_id')
    # cp_output = models.ForeignKey('ReportsResult', models.DO_NOTHING, related_name='reportsresult_action_points_actionpoint_cp_output_id', blank=True, null=True)
    # engagement = models.ForeignKey('AuditEngagement', models.DO_NOTHING, related_name='auditengagement_action_points_actionpoint_engagement_id', blank=True, null=True)
    # intervention = models.ForeignKey('PartnersIntervention', models.DO_NOTHING, related_name='partnersintervention_action_points_actionpoint_intervention_id', blank=True, null=True)
    # location = models.ForeignKey('LocationsLocation', models.DO_NOTHING, related_name='locationslocation_action_points_actionpoint_location_id', blank=True, null=True)
    # office = models.ForeignKey('UsersOffice', models.DO_NOTHING, related_name='usersoffice_action_points_actionpoint_office_id', blank=True, null=True)
    # partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='partnerspartnerorganization_action_points_actionpoint_partner_id', blank=True, null=True)
    # section = models.ForeignKey('ReportsSector', models.DO_NOTHING, related_name='reportssector_action_points_actionpoint_section_id', blank=True, null=True)
    # tpm_activity = models.ForeignKey('TpmTpmactivity', models.DO_NOTHING, related_name='tpmtpmactivity_action_points_actionpoint_tpm_activity_id', blank=True, null=True)
    # high_priority = models.BooleanField()
    # travel_activity = models.ForeignKey('T2FTravelactivity', models.DO_NOTHING, related_name='t2ftravelactivity_action_points_actionpoint_travel_activity_id', blank=True, null=True)
    # category = models.ForeignKey('CategoriesCategory', models.DO_NOTHING, related_name='categoriescategory_action_points_actionpoint_category_id', blank=True, null=True)

    class Options:
        source = ActionPointsActionpoint
        mapping = add_location_mapping(dict(
            author_username='author.username',
            assigned_by_username='assigned_by.username',
            assigned_to_username='assigned_to.username',
            intervention_source_id='intervention.id',
            intervention_number='intervention.number',
            office='office.name',
            partner_source_id='partner.id',
            partner_name='partner.name',
            engagement_source_id='engagement.id',
            engagement_type='engagement.type',
            section_source_id='sector.id',
            section_type='sector.name',
            travel_activity_source_id='travel_activity.id',
            travel_activity_travel_type='travel_activity.travel_type',
            category_source_id='category.id',
            category_module='category.module',

        ))
