from django import forms

from unicef_rest_framework.forms import DateRangePickerField

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.api.endpoints.rapidpro._base_ import RapidProViewSet
from etools_datamart.apps.mart.rapidpro import models


class ContactSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.Contact
        exclude = ()


class ContactFilterForm(forms.Form):
    organization = DateRangePickerField(label='Created between', required=False)


class ContactViewSet(RapidProViewSet):
    serializer_class = ContactSerializer
    queryset = models.Contact.objects.all()
    filter_fields = ('organization', )
    serializers_fieldsets = {'std': ContactSerializer}
    querystringfilter_form_base_class = ContactFilterForm

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)
