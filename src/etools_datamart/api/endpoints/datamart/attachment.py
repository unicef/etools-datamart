from django import forms

from constance import config
from rest_framework import serializers

from unicef_rest_framework.forms import DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class AttachmentSerializerFull(DataMartSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return "%s%s?schema=%s" % (config.ETOOLS_ADDRESS,
                                   obj.file_link,
                                   obj.schema_name)

    class Meta(DataMartSerializer.Meta):
        model = models.Attachment


class AttachmentSerializer(AttachmentSerializerFull):
    class Meta(DataMartSerializer.Meta):
        model = models.Attachment
        exclude = ('schema_name', 'file_type_id')


class AttachmentSerializerEtools(AttachmentSerializerFull):
    attachment = serializers.IntegerField(source='attachment_source_id')

    class Meta(DataMartSerializer.Meta):
        model = models.Attachment
        exclude = None

        fields = ("schema_name",
                  "file_type_id",
                  "partner",
                  "partner_type",
                  "vendor_number",
                  "pd_ssfa",
                  "pd_ssfa_number",
                  "agreement_reference_number",
                  "object_link",
                  "file_type",
                  "file_link",
                  "filename",
                  "source",
                  "uploaded_by",
                  "created",
                  "attachment")


class AttachmentFilterForm(forms.Form):
    created = DateRangePickerField(label='Created between', required=False)


class AttachmentViewSet(common.DataMartViewSet):
    serializer_class = AttachmentSerializer
    queryset = models.Attachment.objects.all()
    filter_fields = ('created', 'date_of_completion', 'due_date')
    serializers_fieldsets = {'std': AttachmentSerializer,
                             'full': AttachmentSerializerFull,
                             'etools': AttachmentSerializerEtools
                             }
    querystringfilter_form_base_class = AttachmentFilterForm

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)
