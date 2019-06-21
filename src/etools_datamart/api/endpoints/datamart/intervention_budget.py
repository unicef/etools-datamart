from django import forms

from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models
from etools_datamart.apps.etools.models import PartnersIntervention


class InterventionFilterForm(forms.Form):
    status__in = Select2MultipleChoiceField(label='Status',
                                            choices=PartnersIntervention.STATUSES,
                                            required=False)
    last_modify_date = DateRangePickerField(label='Modified between',
                                            required=False)

    start_date = DateRangePickerField(label='Started between',
                                      required=False)
    submission_date = DateRangePickerField(label='Submitted between',
                                           required=False)

    document_type__in = Select2MultipleChoiceField(label='Document Type',
                                                   choices=PartnersIntervention.INTERVENTION_TYPES,
                                                   required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if 'status__in' in filters:
            filters.setlist('status__in', data['status__in'].split(','))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class InterventionSerializerBudget(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.InterventionBudget
        exclude = None
        fields = ('number', 'title', 'status', 'start_date', 'end_date',
                  'partner_contribution', 'unicef_cash', 'in_kind_amount',
                  'partner_contribution_local', 'unicef_cash_local', 'in_kind_amount_local',
                  'total', 'total_local', 'currency',
                  )


class InterventionSerializerV2(DataMartSerializer):
    # vendor_number = serializers.CharField(source='vendor_number')
    pd_ssfa_type = serializers.CharField(source='doocument_type')
    pd_ssfa_reference_number = serializers.CharField(source='reference_number')
    pd_ssfa_title = serializers.CharField(source='title')
    pd_ssfa_status = serializers.CharField(source='status')
    pd_ssfa_start_date = serializers.CharField(source='start_date')
    pd_ssfa_end_date = serializers.CharField(source='end_date')
    pd_ssfa_submission_date = serializers.CharField(source='submission_date')
    pd_ssfa_submission_date_prc = serializers.CharField(source='submission_date_prc')

    class Meta:
        model = models.Intervention
        fields = ('partner_name',  # agreement.partner.name
                  'partner_vendor_number',  # agreement.partner.vendor_number
                  'partner_type',  # agreement.partner.partner_type
                  'cso_type',  # agreement.partner.cso_type
                  'country_name',
                  'schema_name',
                  'area_code',
                  'agreement_reference_number',  # agreement.reference_number
                  'pd_ssfa_type',  # doocument_type
                  'reference_number',  # reference_number
                  'pd_ssfa_title',  # title
                  'offices',  # offices (m2m)
                  'unicef_focal_points',  # unicef_focal_points (m2m)
                  # 'unicef_focal_point_email',
                  'partner_focal_points',  # partner_focal_points (m2m)
                  # 'partner_focal_point_email',
                  'pd_ssfa_status',  # status
                  'pd_ssfa_start_date',  # start_date
                  'pd_ssfa_end_date',  # end_date
                  'contingency_pd',  # contingency_pd
                  'country_programme',  # country_programme.name
                  'country_programme_id',  # country_programme_id
                  'clusters',
                  'sections',
                  'cp_output',
                  'cp_output_id',
                  'planned_programmatic_visits',
                  'submission_date',  # submission_date
                  'submission_date_prc',  # submission_date_prc
                  'review_date_prc',
                  'prc_review_document',
                  'partner_signatory_name',
                  'partner_signatory_email',
                  'signed_by_partner_date',  # signed_by_partner_date
                  'unicef_signatory_name',  # unicef_signatory.username
                  'unicef_signatory_email',  # unicef_signatory.mail
                  'signed_by_unicef_date',  # signed_by_unicef_date
                  'days_from_prc_review_to_signature',
                  'days_from_submission_to_signature',
                  'signed_pd_document',
                  'number_of_amendments',
                  'amendment_types',
                  'last_amendment_date',
                  'fr_number',
                  'number_of_attachments',
                  'attachment_type',
                  'created',  # created
                  'updated',  # updated
                  'pd_ssfa_last_modify_date',
                  'pd_ssfa_url',
                  )
