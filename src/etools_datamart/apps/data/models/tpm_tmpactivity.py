from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from etools_datamart.apps.data.loader import Loader
from etools_datamart.apps.data.models.base import DataMartModel
from etools_datamart.apps.etools.models import AttachmentsAttachment, DjangoContentType, TpmTpmactivity


class TPMActivityLoader(Loader):
    @cached_property
    def _ct(self):
        return DjangoContentType.objects.get(app_label='tpm',
                                             model='tpmvisit')

    # def get_pd_ssfa_reference_number(self, original: TpmTpmactivity, values: dict):
    #     return reference_number(original.activity.intervention)

    def get_attachments(self, original: TpmTpmactivity, values: dict):
        attachments = AttachmentsAttachment.objects.filter(object_id=original.tpm_visit.id,
                                                           code='activity_attachments',
                                                           content_type=self._ct,
                                                           ).order_by('id').values_list('file', flat=True)
        return ", ".join(attachments)

    def get_offices(self, original: TpmTpmactivity, values: dict):
        locs = []
        for office in original.offices.select_related('zonal_chief').order_by('id'):
            locs.append(dict(
                source_id=office.id,
                name=office.name,
                zonal_chief=getattr(office.zonal_chief, 'email', None)
            ))
        values['offices_data'] = locs
        return ", ".join([l['name'] for l in locs])

    def get_unicef_focal_points(self, original: TpmTpmactivity, values: dict):
        # TpmTpmactivityUnicefFocalPoints
        ret = []
        for i in original.unicef_focal_points.all():
            ret.append(i.email)

        return ", ".join(ret)

    def get_tpm_focal_points(self, original: TpmTpmactivity, values: dict):
        # tpm_partner : TpmpartnersTpmpartner =
        # staffmembers = TpmTpmvisitTpmPartnerFocalPoints.objects.filter(tpmvisit=original.tpm_visit)
        ret = []
        for member in original.visit.tpm_partner_focal_points.all():
            ret.append(member.user.email)

        values['tpm_focal_points_data'] = ret
        return ",".join(ret)

    def get_locations(self, original: TpmTpmactivity, values: dict):
        # PartnersInterventionFlatLocations
        locs = []
        # intervention: PartnersIntervention = original.activity.intervention
        for location in original.activity.locations.select_related('gateway').order_by('id'):
            locs.append(dict(
                source_id=location.id,
                name=location.name,
                pcode=location.p_code,
                level=location.level,
                levelname=location.gateway.name
            ))
        values['locations_data'] = locs
        return ", ".join([l['name'] for l in locs])

    def process_country(self):
        qs = self.filter_queryset(self.get_queryset())
        for tpm_activity in qs.all().order_by('activity_ptr'):
            # base = activity.activity_ptr
            tpm_activity.visit = tpm_activity.tpm_visit
            tpm_activity.id = tpm_activity.activity.id
            # tpm_activity.activity = tpm_activity.activity_ptr
            # tpm_activities = TpmTpmactivity.objects.filter(tpm_visit=visit).order_by('activity_ptr_id')
            # source = ActivitiesActivity.objects.filter(activitiesactivity_tpm_tpmactivity_activity_ptr_id__tpm_visit=visit)
            # for activity in TpmTpmactivity.objects.filter(tpm_visit=visit):
            #     TODO: remove me
            # print(111, "tpm_tmpvisit.py:22", activity)

            # visit.tpm_activity = tpm_activities.first()
            # if not visit.tpm_activity:
            #     continue

            # visit.activity = visit.tpm_activity.activity_ptr
            # try:
            #     tpm_activity.start_date = tpm_activities.aggregate(date__min=models.Max('activity_ptr__date'))['date__min']
            # except KeyError:
            #     pass
            #
            # tpm_activity.end_date = tpm_activities.aggregate(date__max=models.Max('activity_ptr__date'))['date__max']
            #
            # unicef_focal_points = []
            # for a in tpm_activities.only('activity_ptr_id'):
            #     qs = TpmTpmactivityUnicefFocalPoints.objects.filter(tpmactivity_id=a.activity_ptr_id)
            #     unicef_focal_points.extend(qs.values_list('user__email', flat=True))

            # tpm_activity.unicef_focal_points = ",".join(unicef_focal_points)

            # try:
            #     tpm_activity.report_attachments = ",".join(AttachmentsAttachment.objects.filter(
            #         object_id=visit.id,
            #         code='activity_report',
            #         content_type=content_type
            #     ).values_list('file', flat=True)).strip()
            # except Exception as e:
            #     process_exception(e)
            # try:
            #     visit.attachments = ",".join(AttachmentsAttachment.objects.filter(
            #         object_id=visit.id,
            #         code='activity_attachments',
            #         content_type=content_type
            #     ).values_list('file', flat=True)).strip()
            # except Exception as e:
            #     process_exception(e)

            filters = self.config.key(self, tpm_activity)
            values = self.get_values(tpm_activity)
            op = self.process_record(filters, values)
            self.increment_counter(op)


class TPMActivity(DataMartModel):
    additional_information = models.CharField(max_length=500, blank=True, null=True)
    approval_comment = models.TextField(blank=True, null=True)
    area_code = models.CharField(max_length=500, blank=True, null=True)
    attachments = models.TextField(blank=True, null=True)
    author_name = models.CharField(max_length=120, blank=True, null=True)
    cancel_comment = models.TextField(blank=True, null=True)
    country_name = models.CharField(max_length=500, blank=True, null=True)
    cp_output = models.CharField(max_length=500, blank=True, null=True)
    cp_output_id = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
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
    report_attachment = models.CharField(max_length=500, blank=True, null=True)
    schema_name = models.CharField(max_length=500, blank=True, null=True)
    section = models.CharField(max_length=500, blank=True, null=True)
    source_partner_id = models.IntegerField(blank=True, null=True, db_index=True)
    start_date = models.DateTimeField(blank=True, null=True)
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
        key = lambda loader, record: dict(country_name=loader.context['country'].name,
                                          schema_name=loader.context['country'].schema_name,
                                          source_id=record.id)

        source = TpmTpmactivity
        mapping = dict(additional_information='additional_information',
                       approval_comment="tpm_visit.approval_comment",
                       # attachments="=",
                       author_name="tpm_visit.author.name",
                       cancel_comment="=",
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
                       reject_comment="reject_comment",
                       report_attachment="=",
                       # schema_name="=",
                       section="section.name",
                       source_partner_id="=",
                       start_date="tpm_visit.start_date",
                       status="tpm_visit.status",
                       task_reference_number="=",
                       # tpm_focal_point_email="=",
                       # tpm_focal_point_name="=",
                       tpm_focal_points="-",
                       tpm_name="=",
                       # unicef_focal_point_email="=",
                       # unicef_focal_point_name="=",
                       unicef_focal_points="=",
                       # vendor_number="=",
                       visit_end_date="tpm_visit.end_date",
                       visit_information="tpm_visit.visit_information",
                       visit_reference_number="tpm_visit.reference_number",
                       visit_start_date="tpm_visit.start_date",
                       visit_status="tpm_visit.status",
                       visit_url="=",
                       )
