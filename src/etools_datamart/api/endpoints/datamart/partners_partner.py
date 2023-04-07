from django import forms
from django.db.models import Q

from rest_framework import serializers

from unicef_rest_framework.forms import CleareableSelect2ChoiceField, DateRangePickerField, Select2MultipleChoiceField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models
from etools_datamart.apps.sources.etools.enrichment.consts import PartnerType

from .. import common


class PartnerSerializerV2(DataMartSerializer):
    email_address = serializers.EmailField(source="email")

    class Meta:
        model = models.Partner
        fields = (
            "partner",
            "vendor_number",
            "position",
            "first_name",
            "last_name",
            "email_address",
            "phone_number",
            "active_staff",
        )


class PartnerSerializerFull(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Partner


class PartnerSerializerStd(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Partner
        exclude = ("planned_engagement", "last_pv_date")


class PartnerSerializerShort(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Partner
        exclude = None
        fields = ("name", "alternate_name", "partner_type", "country", "email")


class PartnerFilterForm(forms.Form):
    partner_type__in = Select2MultipleChoiceField(label="Partner Type", choices=PartnerType.CHOICES, required=False)
    last_modify_date = DateRangePickerField(label="Modified between", required=False)
    hidden = CleareableSelect2ChoiceField(
        required=False,
        choices=(
            (None, "All"),
            (False, "False"),
            (True, "True"),
        ),
    )

    def __init__(self, data=None, files=None, auto_id="id_%s", prefix=None, initial=None, *args, **kwargs):
        filters = data.copy()
        initial = {"hidden": ""}
        if "status__in" in filters:
            filters.setlist("status__in", data["status__in"].split(","))
        super().__init__(filters, files, auto_id, prefix, initial, *args, **kwargs)


class PartnerViewSet(common.DataMartViewSet):
    querystringfilter_form_base_class = PartnerFilterForm

    serializer_class = PartnerSerializerFull
    serializers_fieldsets = {
        "std": PartnerSerializerStd,
        "full": PartnerSerializerFull,
        "short": PartnerSerializerShort,
    }
    queryset = models.Partner.objects.all()
    filter_fields = ("partner_type", "hidden", "cso_type", "rating", "last_modify_date", "reported_cy", "total_ct_cy")
    ordering_fields = ("id", "name")

    def get_querystringfilter_form(self, request, filter):
        return PartnerFilterForm(request.GET, filter.form_prefix)


class PartnerHACTActiveViewSet(PartnerViewSet):
    queryset = models.Partner.objects.filter(Q(reported_cy__gt=0) | Q(total_ct_cy__gt=0))
