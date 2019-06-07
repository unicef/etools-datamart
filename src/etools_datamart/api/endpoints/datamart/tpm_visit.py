# -*- coding: utf-8 -*-
from etools_datamart.api.endpoints.datamart.serializers import DataMartSerializer
from etools_datamart.apps.data import models

from .. import common


class TPMVisitSerializerV2(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.TPMVisit
        exclude = None
        fields = (
            "visit_reference_number",
            "task_reference_number",
            "visit_information",
            "visit_status",
            "visit_start_date",
            "visit_end_date",
            "tpm_name",
            "tpm_focal_points",
            "created",
            "date_of_assigned",
            "date_of_cancelled",
            "date_of_tpm_accepted",
            "date_of_tpm_rejected",
            "date_of_tpm_reported",
            "date_of_tpm_report_rejected",
            "date_of_unicef_approved",
            "deleted_at",
            "partner_name",
            "vendor_number",
            "pd_ssfa_title",
            "pd_ssfa_reference_number",
            "cp_output",
            "cp_output_id",
            "section",
            "date",
            "country_name",
            "schema_name",
            "area_code",
            "location_name",
            "location_pcode",
            "location_level",
            "location_levelname",
            "additional_information",
            "unicef_focal_points",
            "office",
            "is_pv",
            "attachments",
            "report_attachment",
            "visit_url",

        )


class TPMVisitSerializer(DataMartSerializer):
    class Meta(DataMartSerializer.Meta):
        model = models.TPMVisit


class TPMVisitViewSet(common.DataMartViewSet):
    serializer_class = TPMVisitSerializer
    queryset = models.TPMVisit.objects.all()
    filter_fields = ('status', 'date_of_assigned', 'date_of_tpm_accepted',
                     'date_of_tpm_rejected')
    ordering_fields = ("id", "created",)
    serializers_fieldsets = {'std': TPMVisitSerializer,
                             'v2': TPMVisitSerializerV2}
