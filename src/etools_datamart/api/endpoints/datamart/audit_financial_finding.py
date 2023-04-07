from django import forms

from unicef_rest_framework.forms import CleareableSelect2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models
from etools_datamart.apps.sources.etools.enrichment.consts import AuditEngagementConsts

from .. import common


class AuditFinancialFindingSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.AuditFinancialFinding


class AuditFinancialFindingFilterForm(forms.Form):
    status__in = CleareableSelect2MultipleChoiceField(
        required=False,
        choices=AuditEngagementConsts.DISPLAY_STATUSES,
    )

    def __init__(self, data=None, files=None, auto_id="id_%s", prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        if "status__in" in filters:
            filters.setlist("status__in", data["status__in"].split(","))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class AuditFinancialFindingViewSet(common.DataMartViewSet):
    serializer_class = AuditFinancialFindingSerializer
    queryset = models.AuditFinancialFinding.objects.all()
    filter_fields = ("status",)
    serializers_fieldsets = {"std": AuditFinancialFindingSerializer}
    querystringfilter_form_base_class = AuditFinancialFindingFilterForm
