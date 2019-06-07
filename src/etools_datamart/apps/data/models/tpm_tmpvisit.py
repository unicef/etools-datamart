from django.db import models

from crashlog.middleware import process_exception

from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.data.models.mixins import add_location_mapping, LocationMixin
from etools_datamart.apps.etools.models import (AttachmentsAttachment, DjangoContentType, TpmTpmactivity,
                                                TpmTpmactivityUnicefFocalPoints, TpmTpmvisit,
                                                TpmTpmvisitTpmPartnerFocalPoints,)


class TPMVisitLoader(Loader):

    def process_country(self):
        qs = self.filter_queryset(self.get_queryset())
        content_type = DjangoContentType.objects.get(app_label='tpm',
                                                     model='tpmvisit')
        for visit in qs.all():
            tpm_activities = TpmTpmactivity.objects.filter(tpm_visit=visit)
            # source = ActivitiesActivity.objects.filter(activitiesactivity_tpm_tpmactivity_activity_ptr_id__tpm_visit=visit)

            try:
                visit.start_date = tpm_activities.aggregate(date__min=models.Max('activity_ptr__date'))['date__min']
            except KeyError:
                pass

            visit.end_date = tpm_activities.aggregate(date__max=models.Max('activity_ptr__date'))['date__max']

            # unicef_focal_points
            unicef_focal_points = []
            for a in tpm_activities.only('activity_ptr_id'):
                qs = TpmTpmactivityUnicefFocalPoints.objects.filter(tpmactivity_id=a.activity_ptr_id)
                unicef_focal_points.extend(qs.values_list('user__email', flat=True))

            visit.unicef_focal_points = ",".join(unicef_focal_points)

            # unicef_focal_points
            tpm_focal_points = []
            # for a in tpm_activities.only('activity_ptr_id'):
            qs = TpmTpmvisitTpmPartnerFocalPoints.objects.filter(tpmvisit=visit)
            tpm_focal_points.extend(qs.values_list('tpmpartnerstaffmember__user__email', flat=True))

            visit.tpm_focal_points = ",".join(tpm_focal_points)
            try:
                visit.report_attachments = ",".join(AttachmentsAttachment.objects.filter(
                    object_id=visit.id,
                    code='activity_report',
                    content_type=content_type
                ).values_list('file', flat=True)).strip()
            except Exception as e:
                process_exception(e)
            try:
                visit.attachments = ",".join(AttachmentsAttachment.objects.filter(
                    object_id=visit.id,
                    code='activity_attachments',
                    content_type=content_type
                ).values_list('file', flat=True)).strip()
            except Exception as e:
                process_exception(e)
            filters = self.config.key(self, visit)
            values = self.get_values(visit)
            op = self.process_record(filters, values)
            self.increment_counter(op)


class TPMVisit(LocationMixin, DataMartModel):
    deleted_at = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    unicef_focal_points = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, blank=True, null=True)
    reject_comment = models.TextField(blank=True, null=True)
    approval_comment = models.TextField(blank=True, null=True)
    visit_information = models.TextField(blank=True, null=True)
    date_of_assigned = models.DateField(blank=True, null=True)
    date_of_cancelled = models.DateField(blank=True, null=True)
    date_of_tpm_accepted = models.DateField(blank=True, null=True)
    date_of_tpm_rejected = models.DateField(blank=True, null=True)
    date_of_tpm_reported = models.DateField(blank=True, null=True)
    date_of_tpm_report_rejected = models.DateField(blank=True, null=True)
    date_of_unicef_approved = models.DateField(blank=True, null=True)
    partner_name = models.CharField(max_length=120, blank=True, null=True)
    vendor_number = models.CharField(max_length=120, blank=True, null=True)
    cancel_comment = models.TextField(blank=True, null=True)
    author_name = models.CharField(max_length=120, blank=True, null=True)

    attachments = models.TextField(blank=True, null=True)
    report_attachment = models.TextField(blank=True, null=True)

    source_partner_id = models.IntegerField(blank=True, null=True, db_index=True)

    visit_reference_number = models.CharField(max_length=300, blank=True, null=True)
    task_reference_number = models.CharField(max_length=300, blank=True, null=True)
    # visit_information = models.TextField(blank=True, null=True)
    visit_status = models.CharField(max_length=300, blank=True, null=True)
    visit_start_date = models.DateField(blank=True, null=True)
    visit_end_date = models.DateField(blank=True, null=True)
    tpm_name = models.CharField(max_length=300, blank=True, null=True)
    tpm_focal_points = models.TextField(blank=True, null=True)

    # created = models.CharField(max_length=300, blank=True, null=True)
    # date_of_assigned = models.DateField(blank=True, null=True)
    # date_of_cancelled = models.DateField(blank=True, null=True)
    # date_of_tpm_accepted = models.DateField(blank=True, null=True)
    # date_of_tpm_rejected = models.DateField(blank=True, null=True)
    # date_of_tpm_reported = models.DateField(blank=True, null=True)
    # date_of_tpm_report_rejected = models.DateField(blank=True, null=True)
    # date_of_unicef_approved = models.DateField(blank=True, null=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)
    # partner_name = models.CharField(max_length=300, blank=True, null=True)
    # vendor_number = models.CharField(max_length=300, blank=True, null=True)
    pd_ssfa_title = models.CharField(max_length=300, blank=True, null=True)
    pd_ssfa_reference_number = models.CharField(max_length=300, blank=True, null=True)
    cp_output = models.CharField(max_length=300, blank=True, null=True)
    cp_output_id = models.CharField(max_length=300, blank=True, null=True)
    section = models.CharField(max_length=300, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    country_name = models.CharField(max_length=300, blank=True, null=True)
    schema_name = models.CharField(max_length=300, blank=True, null=True)
    area_code = models.CharField(max_length=300, blank=True, null=True)
    # location_name = models.CharField(max_length=300, blank=True, null=True)
    # location_pcode = models.CharField(max_length=300, blank=True, null=True)
    # location_level = models.CharField(max_length=300, blank=True, null=True)
    # location_levelname = models.CharField(max_length=300, blank=True, null=True)
    additional_information = models.CharField(max_length=300, blank=True, null=True)
    # unicef_focal_points = models.TextField(blank=True, null=True)
    office = models.CharField(max_length=300, blank=True, null=True)
    is_pv = models.CharField(max_length=300, blank=True, null=True)
    # attachments = models.CharField(max_length=300, blank=True, null=True)
    # report_attachment = models.CharField(max_length=300, blank=True, null=True)
    visit_url = models.CharField(max_length=300, blank=True, null=True)

    loader = TPMVisitLoader()

    class Options:
        # depends = (Intervention,)
        truncate = True
        sync_deleted_records = lambda a: False

        source = TpmTpmvisit
        mapping = add_location_mapping(dict(
            author_name='author.name',
            visit_reference_number='reference_number',
            partner_name='tpm_partner.name',
            vendor_number='tpm_partner.vendor_number',
        ))
