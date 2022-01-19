from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Count, JSONField
from django.utils.translation import gettext as _

from model_utils import Choices

from etools_datamart.apps.mart.data.loader import EtoolsLoader
from etools_datamart.apps.mart.data.models.base import EtoolsDataMartModel
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts, RiskConst
from etools_datamart.apps.sources.etools.models import (
    ActionPointsActionpoint,
    AuditAudit,
    AuditEngagement,
    AuditEngagementActivePd,
    AuditMicroassessment,
    AuditRisk,
    AuditSpecialaudit,
    AuditSpotcheck,
    DjangoContentType,
    UnicefAttachmentsAttachment,
)

from .partner import Partner

attachment_codes = {AuditAudit: 'audit_final_report',
                    AuditMicroassessment: 'micro_assessment_final_report',
                    AuditSpecialaudit: 'special_audit_final_report',
                    AuditSpotcheck: 'spotcheck_final_report',
                    }

URLMAP = {'AuditSpotcheck': "%s/ap/spot-checks/%s/overview/?schema=%s",
          'AuditMicroassessment': "%s/ap/micro-assessments/%s/overview/?schema=%s",
          'AuditSpecialaudit': "%s/ap/special-audits/%s/overview/?schema=%s",
          'AuditAudit': "%s/ap/audits/%s/overview/?schema=%s",
          'TpmTpmactivity': "%s/t2f/edit-travel/%s/?schema=%s",
          'T2FTravelactivity': "%s/t2f/edit-travel/%s/?schema=%s"}

MODULEMAP = {'AuditSpotcheck': "fam",
             'AuditMicroassessment': "fam",
             'AuditSpecialaudit': "fam",
             'AuditAudit': "fam",
             'TpmTpmactivity': "tpm",
             'T2FTravelactivity': "trips"}


class EngagementMixin:
    OVERALL_RISK_MAP = {}

    def get_partner(self, record: AuditEngagement, values: dict, **kwargs):
        try:
            p = Partner.objects.get(
                schema_name=self.context['country'].schema_name,
                source_id=record.partner.pk)
            return {
                'name': p.name,
                'vendor_number': p.vendor_number,
                'id': p.pk,
                'source_id': p.source_id,
                'type': p.partner_type,
                'cso_type': p.cso_type,
                'reported_cy': str(p.reported_cy),
                'total_ct_cy': str(p.total_ct_cy),
            }
        except Partner.DoesNotExist:
            return {key: 'N/A' for key in ['name', 'vendor_number', 'id', 'source_id', 'type', 'cso_type',
                                           'reported_cy', 'total_ct_cy']}

    def _get_risk(self, record: AuditEngagement, **kwargs):
        try:
            risk = AuditRisk.objects.get(
                engagement=record,
                **kwargs
            )
            extra = risk.extra
            value = risk.value
            text = RiskConst.VALUES[value]
        except AuditRisk.DoesNotExist:
            extra, value, text = "", "", ""
        return value, extra, text

    def _get_risks(self, record: AuditEngagement, **kwargs):
        try:
            risks = AuditRisk.objects.filter(
                engagement=record,
                **kwargs
            )
            value = ', '.join([risk.blueprint.header for risk in risks])
            count = risks.count()
        except AuditRisk.DoesNotExist:
            value, count = "", -1
        return value, count

    def get_rating(self, record: AuditEngagement, values: dict, **kwargs):
        filters = {'blueprint__category__code': "ma_global_assessment"}
        value, extra, text = self._get_risk(record, **filters)
        values["rating_extra"] = extra
        return text

    def get_sections(self, record: AuditEngagement, values: dict, **kwargs):
        data = []
        for rec in record.AuditEngagementSections_engagement.all():
            data.append(
                dict(
                    source_id=rec.section.pk,
                    name=rec.section.name,
                    description=rec.section.description,
                ),
            )
        values['sections_data'] = data
        return ", ".join([loc['name'] for loc in data])

    def get_offices(self, record: AuditEngagement, values: dict, **kwargs):
        data = []
        for rec in record.AuditEngagementOffices_engagement.all():
            data.append(dict(source_id=rec.office.id,
                             name=rec.office.name,
                             ))
        values['offices_data'] = data
        return ", ".join([office['name'] for office in data])

    def get_action_points(self, record, values, **kwargs):
        aggr = "category__description"
        st, pr = 'status', 'high_priority'
        qs = ActionPointsActionpoint.objects.filter(engagement=record)
        by_status = list(qs.order_by(st).values(st).annotate(count=Count(st)))
        by_priority = list(qs.order_by(pr).values(pr).annotate(count=Count(pr)))
        values['action_points_data'] = by_status + by_priority
        return list(qs.order_by(aggr).values(aggr).annotate(count=Count(aggr)))


class EngagementlLoader(EngagementMixin, EtoolsLoader):
    def get_queryset(self):
        return AuditEngagement.objects.select_related(
            'partner',
            'agreement',
            'po_item',
            'risks',
        ).all()

    def get_content_type(self, sub_type):
        mapping = {AuditAudit: 'audit',
                   AuditEngagement: 'engagement',
                   AuditMicroassessment: 'microassessment',
                   AuditSpecialaudit: 'specialaudit',
                   AuditSpotcheck: 'spotcheck',
                   }
        return DjangoContentType.objects.get(app_label='audit',
                                             model=mapping[sub_type])

    def get_reference_number(self, record: AuditEngagement, values: dict, **kwargs):
        engagement_code = 'a' if record.engagement_type == AuditEngagementConsts.TYPE_AUDIT else record.engagement_type
        return "/".join([self.context['country'].country_short_code,
                         record.partner.name[:5],
                         engagement_code.upper(),
                         str(record.created.year),
                         str(record.id)
                         ])
        # return '{}/{}/{}/{}/{}'.format(
        #     self.context['country'].short_code,
        #     # connection.tenant.country_short_code or '',
        #     original.partner.name[:5],
        #     engagement_code.upper(),
        #     original.created.year,
        #     original.id
        # )

    def get_engagement_attachments(self, record: AuditEngagement, values: dict, **kwargs):
        # audit_engagement
        ret = UnicefAttachmentsAttachment.objects.filter(
            object_id=record.id,
            code='audit_engagement',
            content_type=self.get_content_type(AuditEngagement)).values_list('file', flat=True)

        return ", ".join(ret)

    def get_report_attachments(self, record: AuditEngagement, values: dict, **kwargs):
        # audit_report
        ret = UnicefAttachmentsAttachment.objects.filter(
            object_id=record.id,
            code='audit_report',
            content_type=self.get_content_type(AuditEngagement)).values_list('file', flat=True)

        return ", ".join(ret)

    def get_final_report(self, record: AuditEngagement, values: dict, **kwargs):
        if getattr(record._impl, 'final_report', None):
            return UnicefAttachmentsAttachment.objects.get(
                object_id=record.id,
                code=attachment_codes[record.sub_type],
                content_type=self.get_content_type(record.sub_type)).file

    def get_values(self, record: AuditEngagement):
        values = {}
        self.mapping.update(**values)
        return super().get_values(record)

    def get_authorized_officers(self, record: AuditEngagement, values: dict, **kwargs):
        ret = []
        for o in record.authorized_officers.all():
            ret.append({'last_name': o.last_name,
                        'first_name': o.first_name,
                        'partner': o.partner.name,
                        'email': o.email,
                        })
        values['authorized_officers_data'] = ret
        return ", ".join([o['email'] for o in ret])

    def get_active_pd(self, record: AuditEngagement, values: dict, **kwargs):
        ret = []
        for o in (AuditEngagementActivePd.objects
                  .select_related('intervention')
                  .filter(engagement=record)):
            ret.append({'title': o.intervention.title,
                        'number': o.intervention.number,
                        'status': o.intervention.status,
                        'document_type': o.intervention.document_type,
                        })

        values['active_pd_data'] = ret
        return ", ".join([o['number'] for o in ret])

    def get_partner_id(self, record: AuditEngagement, values: dict, **kwargs):
        try:
            return Partner.objects.get(
                schema_name=self.context['country'].schema_name,
                source_id=record.partner.id).pk
        except Partner.DoesNotExist:
            return None

    def get_staff_members(self, record: AuditEngagement, values: dict, **kwargs):
        ret = []
        for o in record.staff_members.all():
            ret.append({'last_name': o.user.last_name,
                        'first_name': o.user.first_name,
                        'email': o.user.email,
                        })
        values['staff_members_data'] = ret
        return ", ".join([o['email'] for o in ret])

    # def get_active_pd(self, original: AuditEngagement, values: dict):
    #     return None

    def get_action_points(self, record: AuditEngagement, values: dict, **kwargs):
        from etools_datamart.api.endpoints.datamart.actionpoint import ActionPointSimpleSerializer

        ret = []
        for r in ActionPointsActionpoint.objects.filter(engagement=record).all():
            ret.append(ActionPointSimpleSerializer(r).data)
        return ret

    def process_country(self):
        for m in [AuditMicroassessment, AuditSpecialaudit, AuditSpotcheck, AuditAudit]:
            for record in m.objects.select_related('engagement_ptr'):
                record.id = record.engagement_ptr_id
                record.sub_type = m
                record.engagement_ptr._impl = record
                filters = self.config.key(self, record.engagement_ptr)
                values = self.get_values(record.engagement_ptr)
                op = self.process_record(filters, values)
                self.increment_counter(op)


class Engagement(EtoolsDataMartModel):
    TYPE_AUDIT = 'audit'
    TYPE_MICRO_ASSESSMENT = 'ma'
    TYPE_SPOT_CHECK = 'sc'
    TYPE_SPECIAL_AUDIT = 'sa'

    TYPES = Choices(
        (TYPE_AUDIT, _('Audit')),
        (TYPE_MICRO_ASSESSMENT, _('Micro Assessment')),
        (TYPE_SPOT_CHECK, _('Spot Check')),
        (TYPE_SPECIAL_AUDIT, _('Special Audit')),
    )

    # DISPLAY_STATUSES = Choices(
    #     ('partner_contacted', _('IP Contacted')),
    #     ('field_visit', _('Field Visit')),
    #     ('draft_issued_to_partner', _('Draft Report Issued to IP')),
    #     ('comments_received_by_partner', _('Comments Received from IP')),
    #     ('draft_issued_to_unicef', _('Draft Report Issued to UNICEF')),
    #     ('comments_received_by_unicef', _('Comments Received from UNICEF')),
    #     ('report_submitted', _('Report Submitted')),
    #     ('final', _('Final Report')),
    #     ('cancelled', _('Cancelled')),
    # )
    # DISPLAY_STATUSES_DATES = {
    #     DISPLAY_STATUSES.partner_contacted: 'partner_contacted_at',
    #     DISPLAY_STATUSES.field_visit: 'date_of_field_visit',
    #     DISPLAY_STATUSES.draft_issued_to_partner: 'date_of_draft_report_to_ip',
    #     DISPLAY_STATUSES.comments_received_by_partner: 'date_of_comments_by_ip',
    #     DISPLAY_STATUSES.draft_issued_to_unicef: 'date_of_draft_report_to_unicef',
    #     DISPLAY_STATUSES.comments_received_by_unicef: 'date_of_comments_by_unicef',
    #     DISPLAY_STATUSES.report_submitted: 'date_of_report_submit',
    #     DISPLAY_STATUSES.final: 'date_of_final_report',
    #     DISPLAY_STATUSES.cancelled: 'date_of_cancel'
    # }

    # Base fields
    active_pd = models.TextField(blank=True, null=True)
    active_pd_data = JSONField(blank=True, null=True)
    additional_supporting_documentation_provided = models.DecimalField(blank=True, null=True, decimal_places=2,
                                                                       max_digits=20)
    agreement = models.CharField(max_length=300, blank=True, null=True)
    auditor = models.CharField(max_length=255, blank=True, null=True)
    auditor_number = models.CharField(max_length=30, blank=True, null=True)
    amount_refunded = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    authorized_officers = models.TextField(blank=True, null=True)
    authorized_officers_data = JSONField(blank=True, null=True)
    sections = models.TextField(blank=True, null=True)
    sections_data = JSONField(blank=True, null=True, default=dict)
    cancel_comment = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    date_of_cancel = models.DateField(null=True, blank=True)
    date_of_comments_by_ip = models.DateField(blank=True, null=True)
    date_of_comments_by_unicef = models.DateField(blank=True, null=True)
    date_of_draft_report_to_ip = models.DateField(blank=True, null=True)
    date_of_draft_report_to_unicef = models.DateField(blank=True, null=True)
    date_of_field_visit = models.DateField(blank=True, null=True)
    date_of_final_report = models.DateField(null=True, blank=True)
    date_of_report_submit = models.DateField(null=True, blank=True)
    end_date = models.DateField(blank=True, null=True, db_index=True)
    engagement_attachments = models.TextField(blank=True, null=True)
    engagement_type = models.CharField(max_length=300, blank=True,
                                       null=True, choices=TYPES, db_index=True)
    exchange_rate = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    explanation_for_additional_information = models.TextField(blank=True, null=True)
    joint_audit = models.BooleanField(default=False, blank=True, null=True)
    justification_provided_and_accepted = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20)
    modified = models.DateField(blank=True, null=True)
    partner_contacted_at = models.DateField(blank=True, null=True, db_index=True)
    partner = JSONField(blank=True, null=True, default=dict)
    po_item = models.IntegerField(blank=True, null=True)
    report_attachments = models.TextField(blank=True, null=True)
    staff_members = models.TextField(blank=True, null=True)
    staff_members_data = JSONField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True, db_index=True)
    status = models.CharField(max_length=30, blank=True, null=True,
                              choices=AuditEngagementConsts.DISPLAY_STATUSES,
                              db_index=True)
    total_value = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    write_off_required = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)

    reference_number = models.CharField(max_length=300, blank=True, null=True)

    # final_report is shared across all Engagement types
    final_report = models.CharField(max_length=300, blank=True, null=True)

    shared_ip_with = ArrayField(models.CharField(max_length=20, blank=True, null=True),
                                blank=True, null=True, default=list, verbose_name=_('Shared Audit with'))

    # SpotCheck
    spotcheck_total_amount_tested = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20)
    spotcheck_total_amount_of_ineligible_expenditure = models.DecimalField(null=True, blank=True, decimal_places=2,
                                                                           max_digits=20)
    spotcheck_internal_controls = models.TextField(null=True, blank=True)
    spotcheck_final_report = models.CharField(max_length=300, blank=True, null=True)
    # MicroAssessment
    # final_report = CodedGenericRelation(Attachment, code='micro_assessment_final_report')
    # Audit
    rating = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=RiskConst.VALUES,
    )
    rating_extra = JSONField(blank=True, null=True)

    AUDIT_OPTION_UNQUALIFIED = "unqualified"
    AUDIT_OPTION_QUALIFIED = "qualified"
    AUDIT_OPTION_DENIAL = "disclaimer_opinion"
    AUDIT_OPTION_ADVERSE = "adverse_opinion"

    AUDIT_OPTIONS = Choices(
        (AUDIT_OPTION_UNQUALIFIED, _("Unqualified")),
        (AUDIT_OPTION_QUALIFIED, _("Qualified")),
        (AUDIT_OPTION_DENIAL, _("Disclaimer opinion")),
        (AUDIT_OPTION_ADVERSE, _("Adverse opinion")),
    )

    audited_expenditure = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    financial_findings = models.DecimalField(blank=True, null=True, default=0, decimal_places=2, max_digits=20)
    audit_opinion = models.CharField(max_length=20, choices=AUDIT_OPTIONS,
                                     blank=True, null=True, db_index=True)
    # final_report = CodedGenericRelation(Attachment, code='audit_final_report')

    # SpecialAudit
    # final_report = CodedGenericRelation(Attachment, code='special_audit_final_report')

    # ActionPoints
    action_points = JSONField(blank=True, null=True)

    # datamart
    loader = EngagementlLoader()

    class Meta:
        ordering = ("id",)

    class Options:
        source = AuditEngagement
        sync_deleted_records = lambda a: False
        depends = (Partner,)
        mapping = dict(
            active_pd="-",
            active_pd_data="i",
            agreement="agreement.order_number",  # PurchaseOrder
            auditor="agreement.auditor_firm.name",
            auditor_number="agreement.auditor_firm.vendor_number",
            authorized_officers="-",
            reference_number="-",
            engagement_attachments='-',
            report_attachments='-',
            staff_members='-',
            partner="-",
            po_item="po_item.number",  # PurchaseOrderItem
            final_report="-",
            spotcheck_total_amount_tested='_impl.total_amount_tested',
            spotcheck_total_amount_of_ineligible_expenditure='_impl.total_amount_of_ineligible_expenditure',
            spotcheck_final_report='_impl.final_report',
            spotcheck_internal_controls='_impl.internal_controls',
            audited_expenditure='_impl.audited_expenditure',
            financial_findings='_impl.financial_findings',
            audit_opinion='_impl.audit_opinion',
            action_points="-",
            rating="-",
            rating_extra="i",
        )
