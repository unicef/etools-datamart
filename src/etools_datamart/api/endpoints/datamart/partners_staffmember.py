from rest_framework import serializers

from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.mart.data import models

from .. import common


class PartnerStaffMemberSerializer(DataMartSerializer):
    email_address = serializers.EmailField(source='email')
    position = serializers.CharField(source='title')
    phone_number = serializers.CharField(source='phone')
    active_staff = serializers.CharField(source='active')

    class Meta:
        model = models.PartnerStaffMember
        fields = ('partner',
                  'partner_id',
                  'user',
                  'vendor_number',
                  'position',
                  'first_name',
                  'last_name',
                  'email_address',
                  'phone_number',
                  'active_staff')


class PartnerStaffMemberViewSet(common.DataMartViewSet):
    serializer_class = PartnerStaffMemberSerializer
    queryset = models.PartnerStaffMember.objects.all()
