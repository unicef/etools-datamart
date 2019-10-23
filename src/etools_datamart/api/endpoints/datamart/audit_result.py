from django import forms

from unicef_rest_framework.forms import CleareableSelect2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models
from etools_datamart.apps.etools.enrichment.consts import AuditEngagementConsts

from .. import common


class AuditResultSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.AuditResult


class AuditResultFilterForm(forms.Form):
    status__in = CleareableSelect2MultipleChoiceField(required=False,
                                                      choices=AuditEngagementConsts.DISPLAY_STATUSES,
                                                      )

    risk_rating = CleareableSelect2MultipleChoiceField(required=False,
                                                       choices=(('High', 'High'),
                                                                ('Significant', 'Significant'),
                                                                ('Medium', 'Medium'),
                                                                ('Low', 'Low'),))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if 'status__in' in filters:
            filters.setlist('status__in', data['status__in'].split(','))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class AuditResultViewSet(common.DataMartViewSet):
    serializer_class = AuditResultSerializer
    queryset = models.AuditResult.objects.all()
    filter_fields = ('risk_rating',)
    serializers_fieldsets = {'std': AuditResultSerializer}
    querystringfilter_form_base_class = AuditResultFilterForm

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)

    def get_queryset(self):
        return super().get_queryset()
