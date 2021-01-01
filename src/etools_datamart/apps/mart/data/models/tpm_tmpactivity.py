from django.db import models
from django.db.models import JSONField
from django.utils.functional import cached_property

from dynamic_serializer.core import get_attr

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.models import DjangoContentType, TpmTpmactivity, UnicefAttachmentsAttachment


class TPMActivityLoader(EtoolsLoader):
    @cached_property
    def _ct(self):
        return DjangoContentType.objects.get(app_label='tpm',
                                             model='tpmactivity')

    # def get_pd_ssfa_reference_number(self, original: TpmTpmactivity, values: dict):
    #     return reference_number(original.activity.intervention)

    def get_task_reference_number(self, record: TpmTpmactivity, values: dict, **kwargs):
        return "Task #{}.{}".format(record.tpm_visit.id, record.id)

    def get_visit_url(self, record: TpmTpmactivity, values: dict, **kwargs):
        return 'tpm/visits/%s/details' % record.tpm_visit_id

    def get_report_attachments(self, record: TpmTpmactivity, values: dict, **kwargs):
        # attachments = AttachmentsAttachment.objects.filter(object_id=original.tpm_visit.id,
        #                                                    code='activity_report',
        #                                                    content_type=self._ct,
        #                                                    ).order_by('id').values_list('file', flat=True)
        #
        # values['report_attachments_data'] = attachments
        attachments = (UnicefAttachmentsAttachment.objects
                       .select_related('uploaded_by', 'file_type')
                       .filter(object_id=record.tpm_visit.id,
                               code='activity_report',
                               content_type=self._ct,
                               ).order_by('id'))
        ret = []
        for a in attachments:
            ret.append(dict(
                file=a.file,
                file_type=a.file_type.name,
                code=a.code,
                uploaded_by=get_attr(a, 'uploaded_by.email')
            ))

        values['report_attachments_data'] = ret
        return ", ".join([a.file for a in attachments])

    def get_attachments(self, record: TpmTpmactivity, values: dict, **kwargs):
        attachments = (UnicefAttachmentsAttachment.objects
                       .select_related('uploaded_by', 'file_type')
                       .filter(object_id=record.tpm_visit.id,
                               code='activity_attachments',
                               content_type=self._ct,
                               ).order_by('id'))
        ret = []
        for a in attachments:
            ret.append(dict(
                file=a.file,
                file_type=a.file_type.name,
                code=a.code,
                uploaded_by=get_attr(a, 'uploaded_by.email')
            ))

        values['attachments_data'] = ret
        return ", ".join([a.file for a in attachments])

    def get_offices(self, record: TpmTpmactivity, values: dict, **kwargs):
        locs = []
        for office in record.offices.order_by('id'):
            locs.append(dict(
                source_id=office.id,
                name=office.name,
            ))
        values['offices_data'] = locs
        return ", ".join([l['name'] for l in locs])

    def get_unicef_focal_points(self, record: TpmTpmactivity, values: dict, **kwargs):
        # TpmTpmactivityUnicefFocalPoints
        ret = []
        for i in record.unicef_focal_points.all():
            ret.append(i.email)

        return ", ".join(ret)

    def get_tpm_focal_points(self, record: TpmTpmactivity, values: dict, **kwargs):
        # tpm_partner : TpmpartnersTpmpartner =
        # staffmembers = TpmTpmvisitTpmPartnerFocalPoints.objects.filter(tpmvisit=original.tpm_visit)
        ret = []
        for member in record.visit.tpm_partner_focal_points.all():
            ret.append(dict(email=member.user.email,
                            first_name=member.user.first_name,
                            last_name=member.user.last_name, ))

        values['tpm_focal_points_data'] = ret
        return ",".join([m['email'] for m in ret])

    def get_locations(self, record: TpmTpmactivity, values: dict, **kwargs):
        # PartnersInterventionFlatLocations
        locs = []
        # intervention: PartnersIntervention = original.activity.intervention
        # for location in original.activity.locations.order_by('id'):
        for location in record.activity.locations.order_by('id'):
            locs.append(dict(
                source_id=location.id,
                name=location.name,
                pcode=location.p_code,
                level=location.admin_level,
                levelname=location.admin_level_name
            ))
        values['locations_data'] = locs
        return ", ".join([l['name'] for l in locs])

    def get_queryset(self):
        return TpmTpmactivity.objects.select_related('activity_ptr')

    def process_country(self):
        qs = self.filter_queryset(self.get_queryset())
        for tpm_activity in qs.all():
            tpm_activity.id = tpm_activity.activity_ptr_id
            tpm_activity.activity = tpm_activity.activity_ptr
            tpm_activity.visit = tpm_activity.tpm_visit

            filters = self.config.key(self, tpm_activity)
            values = self.get_values(tpm_activity)
            op = self.process_record(filters, values)
            self.increment_counter(op)


class TPMActivity(EtoolsDataMartModel):
    additional_information = models.TextField(blank=True, null=True)
    approval_comment = models.TextField(blank=True, null=True)
    area_code = models.CharField(max_length=500, blank=True, null=True)
    attachments = models.TextField(blank=True, null=True)
    attachments_data = JSONField(blank=True, null=True)
    author_name = models.CharField(max_length=120, blank=True, null=True)
    cancel_comment = models.TextField(blank=True, null=True)
    country_name = models.CharField(max_length=500, blank=True, null=True)
    cp_output = models.CharField(max_length=500, blank=True, null=True)
    cp_output_id = models.CharField(max_length=500, blank=True, null=True)
    # created = models.DateField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    date_of_assigned = models.DateField(blank=True, null=True)
    date_of_cancelled = models.DateField(blank=True, null=True)
    date_of_tpm_accepted = models.DateField(blank=True, null=True)
    date_of_tpm_rejected = models.DateField(blank=True, null=True)
    date_of_tpm_report_rejected = models.DateField(blank=True, null=True)
    date_of_tpm_reported = models.DateField(blank=True, null=True)
    date_of_unicef_approved = models.DateField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    # end_date = models.DateTimeField(blank=True, null=True)
    is_pv = models.BooleanField(max_length=500, blank=True, null=True)
    locations = models.TextField(blank=True, null=True)
    locations_data = JSONField(blank=True, null=True, default=dict)
    # location_level = models.CharField(max_length=500, blank=True, null=True)
    # location_levelname = models.CharField(max_length=500, blank=True, null=True)
    # location_name = models.CharField(max_length=500, blank=True, null=True)
    # location_pcode = models.CharField(max_length=500, blank=True, null=True)
    offices = models.TextField(blank=True, null=True)
    offices_data = JSONField(blank=True, null=True)
    partner_name = models.CharField(max_length=120, blank=True, null=True)
    partner_vendor_number = models.CharField(max_length=120, blank=True, null=True)
    pd_ssfa_reference_number = models.CharField(max_length=500, blank=True, null=True)
    pd_ssfa_title = models.CharField(max_length=500, blank=True, null=True)
    reject_comment = models.TextField(blank=True, null=True)
    report_attachments = models.TextField(blank=True, null=True)
    report_attachments_data = JSONField(blank=True, null=True)
    schema_name = models.CharField(max_length=500, blank=True, null=True)
    section = models.CharField(max_length=500, blank=True, null=True)
    # source_partner_id = models.IntegerField(blank=True, null=True, db_index=True)
    # start_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    task_reference_number = models.CharField(max_length=500, blank=True, null=True)
    # tpm_focal_point_email = models.CharField(max_length=500, blank=True, null=True)
    # tpm_focal_point_name = models.CharField(max_length=500, blank=True, null=True)
    tpm_focal_points = models.TextField(blank=True, null=True)
    tpm_focal_points_data = JSONField(blank=True, null=True)
    tpm_name = models.CharField(max_length=500, blank=True, null=True)
    # unicef_focal_point_email = models.CharField(max_length=500, blank=True, null=True)
    # unicef_focal_point_name = models.CharField(max_length=500, blank=True, null=True)
    unicef_focal_points = models.TextField(blank=True, null=True)
    # vendor_number = models.CharField(max_length=500, blank=True, null=True)
    visit_created = models.DateTimeField(blank=True, null=True)
    visit_end_date = models.CharField(max_length=500, blank=True, null=True)
    visit_information = models.TextField(blank=True, null=True)
    visit_reference_number = models.CharField(max_length=500, blank=True, null=True)
    visit_start_date = models.CharField(max_length=500, blank=True, null=True)
    visit_status = models.CharField(max_length=500, blank=True, null=True)
    visit_url = models.CharField(max_length=500, blank=True, null=True)

    loader = TPMActivityLoader()

    class Options:
        # depends = (Intervention,)
        # truncate = True
        sync_deleted_records = lambda a: False
        # key = lambda loader, record: dict(schema_name=loader.context['country'].schema_name,
        #                                   source_id=record.id)

        source = TpmTpmactivity
        mapping = dict(additional_information='additional_information',
                       approval_comment="tpm_visit.approval_comment",
                       # attachments="=",
                       author_name="tpm_visit.author.name",
                       cancel_comment="tpm_visit.cancel_comment",
                       # country_name="=",
                       cp_output="activity.cp_output.name",
                       cp_output_id="activity.cp_output.vision_id",
                       # created="=",
                       date="activity.date",
                       date_of_assigned="tpm_visit.date_of_assigned",
                       date_of_cancelled="tpm_visit.date_of_cancelled",
                       date_of_tpm_accepted="tpm_visit.date_of_tpm_accepted",
                       date_of_tpm_rejected="tpm_visit.date_of_tpm_rejected",
                       date_of_tpm_report_rejected="tpm_visit.date_of_tpm_report_rejected",
                       date_of_tpm_reported="tpm_visit.date_of_tpm_reported",
                       date_of_unicef_approved="tpm_visit.date_of_unicef_approved",
                       deleted_at="tpm_visit.deleted_at",
                       # end_date="tpm_visit.end_date",
                       is_pv="is_pv",
                       locations="-",
                       locations_data="i",
                       # location_level="=",
                       # location_levelname="=",
                       # location_name="=",
                       # location_pcode="=",
                       offices="-",
                       offices_data="i",
                       partner_name="activity.partner.name",
                       partner_vendor_number="activity.partner.vendor_number",
                       pd_ssfa_reference_number="activity.intervention.reference_number",
                       pd_ssfa_title="activity.intervention.title",
                       reject_comment="activity.reject_comment",
                       report_attachments="=",
                       # schema_name="=",
                       section="section.name",
                       # source_partner_id="=",
                       # start_date="tpm_visit.start_date",
                       status="tpm_visit.status",
                       task_reference_number="-",
                       # tpm_focal_point_email="=",
                       # tpm_focal_point_name="=",
                       tpm_focal_points="-",
                       tpm_focal_points_data="i",
                       tpm_name="tpm_visit.tpm_partner.name",
                       # unicef_focal_point_email="=",
                       # unicef_focal_point_name="=",
                       unicef_focal_points="=",
                       # vendor_number="=",
                       visit_created="tpm_visit.created",
                       visit_end_date="tpm_visit.end_date",
                       visit_information="tpm_visit.visit_information",
                       visit_reference_number="tpm_visit.reference_number",
                       visit_start_date="tpm_visit.start_date",
                       visit_status="tpm_visit.status",
                       visit_url="=",
                       )
