from django.db import models

from crashlog.middleware import process_exception

from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.data.models.mixins import add_location_mapping, LocationMixin
from etools_datamart.apps.etools.models import (ActivitiesActivity, AttachmentsAttachment,
                                                DjangoContentType, TpmTpmactivity,)


class TPMActivityLoader(Loader):

    def get_queryset(self):
        return ActivitiesActivity.objects.exclude(activitiesactivity_tpm_tpmactivity_activity_ptr_id__isnull=True)

    def process_country(self):
        qs = self.filter_queryset(self.get_queryset())
        content_type = DjangoContentType.objects.get(app_label='tpm',
                                                     model='tpmactivity')
        for activity in qs.all():
            tpm = TpmTpmactivity.objects.select_related('tpm_visit', 'section').get(activity_ptr=activity.id)
            activity.activity_ptr = tpm.activity_ptr.id
            activity.additional_information = tpm.additional_information or 'N/A'
            activity.is_pv = tpm.is_pv
            activity.tpm_visit = tpm.tpm_visit
            activity.section = tpm.section
            for location in activity.locations.order_by('id'):
                for unicef_focal_point in activity.intervention.unicef_focal_points.all():
                    # activity_report
                    try:
                        activity.report_attachments = ",".join(AttachmentsAttachment.objects.filter(
                            object_id=activity.id,
                            code='activity_report',
                            content_type=content_type
                        ).values_list('file', flat=True)).strip()
                    except Exception as e:
                        process_exception(e)
                    try:
                        activity.attachments = ",".join(AttachmentsAttachment.objects.filter(
                            object_id=activity.id,
                            code='activity_attachments',
                            content_type=content_type
                        ).values_list('file', flat=True)).strip()
                    except Exception as e:
                        process_exception(e)
                    activity.location = location
                    activity.unicef_focal_point = unicef_focal_point
                    filters = self.config.key(self, activity)
                    values = self.get_values(activity)
                    op = self.process_record(filters, values)
                    self.increment_counter(op)


class TPMActivity(LocationMixin, DataMartModel):
    date = models.DateField(blank=True, null=True)
    # cp_output = models.ForeignKey('ReportsResult', models.DO_NOTHING, related_name='reportsresult_activities_activity_cp_output_id', blank=True, null=True)
    # tpm_visit = models.ForeignKey('TpmTpmvisit', models.DO_NOTHING, related_name='tpmtpmvisit_tpm_tpmactivity_tpm_visit_id')
    # partner = models.ForeignKey('PartnersPartnerorganization', models.DO_NOTHING, related_name='partnerspartnerorganization_activities_activity_partner_id', blank=True, null=True)
    # activity_ptr = models.OneToOneField(ActivitiesActivity, models.DO_NOTHING, related_name='activitiesactivity_tpm_tpmactivity_activity_ptr_id')

    additional_information = models.TextField(blank=True, null=True)
    is_pv = models.BooleanField(blank=True, null=True)
    intervention_number = models.CharField(max_length=128, blank=True, null=True)
    result_name = models.CharField(max_length=128, blank=True, null=True)
    partner_name = models.CharField(max_length=128, blank=True, null=True)
    unicef_focal_point_name = models.CharField(max_length=128, blank=True, null=True)
    visit_status = models.CharField(max_length=128, blank=True, null=True)
    visit_information = models.CharField(max_length=128, blank=True, null=True)
    section_name = models.CharField(max_length=128, blank=True, null=True)

    source_visit_id = models.IntegerField(blank=True, null=True)
    source_result_id = models.IntegerField(blank=True, null=True)
    source_partner_id = models.IntegerField(blank=True, null=True)
    source_intervention_id = models.IntegerField(blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)

    # attachments = CodedGenericRelation(Attachment, verbose_name=_('Activity Attachments'),
    #                                    code='activity_attachments', blank=True)
    # report_attachments = CodedGenericRelation(Attachment, verbose_name=_('Activity Report'),
    #                                           code='activity_report', blank=True)
    # attachments = JSONField(blank=True, null=True)
    # report_attachment = JSONField(blank=True, null=True)
    attachments = models.TextField(blank=True, null=True)
    report_attachment = models.TextField(blank=True, null=True)

    loader = TPMActivityLoader()

    class Options:
        # we need TpmTpmactivity
        source = ActivitiesActivity
        sync_deleted_records = lambda a: False
        truncate = True
        mapping = add_location_mapping(dict(section_name='section.name',
                                            intervention_number='intervention.number',
                                            partner_name='partner.name',
                                            result_name='cp_output.name',
                                            visit_status='visit.status',
                                            visit_information='visit.visit_information',
                                            source_visit_id='tpm_visit.id',
                                            source_result_id='cp_output.id',
                                            source_partner_id='partner.id',
                                            source_intervention_id='intervention.id',
                                            source_id='activity_ptr',
                                            unicef_focal_point_name='unicef_focal_point.name'
                                            ))
