from django import forms

from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common

URLMAP = {'AuditSpotcheck': "https://etools.unicef.org/ap/spot-checks/%s/overview",
          'AuditMicroassessment': "https://etools.unicef.org/ap/micro-assessments/%s/overview",
          'AuditSpecialaudit': "https://etools.unicef.org/ap/special-audits/%s/overview",
          'AuditAudit': "https://etools.unicef.org/audits/%s/overview",
          'TpmTpmactivity': "",
          'T2FTravelactivity': "https://etools.unicef.org/t2f/edit-travel/%s"}


class ActionPointSerializerV2(DataMartSerializer):
    section = serializers.CharField(source='section_type')
    pd_ssfa_title = serializers.CharField(source='intervention_title')
    pd_ssfa_reference_number = serializers.CharField(source='intervention_title')
    fam_category = serializers.CharField(source='category_description')
    action_point_url = serializers.SerializerMethodField()
    related_module_url = serializers.SerializerMethodField()

    def get_action_point_url(self, obj):
        return "https://etools.unicef.org/apd/action-points/detail/%s" % obj.source_id

    def get_related_module_url(self, obj):
        base_url = URLMAP[obj.related_module_class]
        return base_url % obj.source.id

    class Meta(DataMartSerializer.Meta):
        model = models.ActionPoint
        exclude = None
        fields = ('reference_number',
                  'created',
                  'status',
                  'assigned_by_name',
                  'assigned_by_email',
                  'assigned_to_name',
                  'assigned_to_email',
                  'office',
                  'section',
                  'due_date',
                  'date_of_completion',
                  'high_priority',
                  'description',
                  'actions_taken',
                  'country_name',
                  'area_code',
                  'location_name',
                  'location_pcode',
                  'location_level',
                  'location_levelname',
                  'partner_name',
                  'vendor_number',
                  'cp_output',
                  'cp_output_id',
                  'pd_ssfa_title',
                  'pd_ssfa_reference_number',
                  'category_module',
                  'module_reference_number',
                  'module_task_activity_reference_number',
                  'fam_category',
                  'related_module_url',
                  'action_point_url')


class ActionPointSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.ActionPoint
        exclude = None
        fields = '__all__'


class ActionPointFilterForm(forms.Form):
    last_modify_date = DateRangePickerField(label='Modified between',
                                            required=False)

    start_date = DateRangePickerField(label='Started between',
                                      required=False)
    submission_date = DateRangePickerField(label='Submitted between',
                                           required=False)

    # document_type__in = Select2MultipleChoiceField(label='Document Type',
    #                                                choices=PartnersIntervention.INTERVENTION_TYPES,
    #                                                required=False)


class ActionPointViewSet(common.DataMartViewSet):
    serializer_class = ActionPointSerializer
    queryset = models.ActionPoint.objects.all()
    filter_fields = ('vendor_code', 'fr_type', 'start_date')
    serializers_fieldsets = {'std': ActionPointSerializer,
                             'v2': ActionPointSerializerV2}

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)
