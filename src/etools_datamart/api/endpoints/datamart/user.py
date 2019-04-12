# -*- coding: utf-8 -*-
from functools import lru_cache

from django import forms

from unicef_rest_framework.ds import DynamicSerializerFilter
from unicef_rest_framework.forms import DateRangePickerField
from unicef_rest_framework.ordering import OrderingFilter

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.api.filtering import CountryNameFilter, DatamartQueryStringFilterBackend
from etools_datamart.apps.data import models
from etools_datamart.apps.etools.models import UsersOffice

from .. import common


@lru_cache()
def get_all_offices():
    names = UsersOffice.objects.values_list('name', flat=True)
    return zip(names, names)


class EtoolsUserFilterForm(forms.Form):
    last_login = DateRangePickerField(label='Last login',
                                      required=False)
    # office__in = Select2MultipleChoiceField(label='Office',
    #                                         choices=SimpleLazyObject(get_all_offices),
    #                                         required=False)


class EtoolsUserSerializerFull(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.EtoolsUser
        read_only = ['last_modify_date', ]
        exclude = ('phone_number',)


class EtoolsUserSerializerStd(EtoolsUserSerializerFull):
    pass


class EtoolsUserViewSet(common.DataMartViewSet):
    serializer_class = EtoolsUserSerializerStd
    filter_backends = [CountryNameFilter,
                       DatamartQueryStringFilterBackend,
                       OrderingFilter,
                       DynamicSerializerFilter,
                       ]

    queryset = models.EtoolsUser.objects.all()
    filter_fields = ('last_modify_date', 'office')
    serializers_fieldsets = {"std": None,
                             "full": EtoolsUserSerializerFull,
                             }

    def get_querystringfilter_form(self, request, filter):
        return EtoolsUserFilterForm(request.GET, filter.form_prefix)
