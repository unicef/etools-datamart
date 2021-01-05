from django.contrib.postgres.fields import JSONField
from django.db import models

from etools_datamart.apps.etl.loader import CommonLoader
from etools_datamart.apps.mart.unpp.base import UNPPDataMartModel
from etools_datamart.apps.sources.unpp.models import CommonPoint, ProjectApplication


class Location(UNPPDataMartModel):
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=3, blank=True, null=True)

    loader = CommonLoader()

    class Meta:
        app_label = 'unpp'

    class Options:
        key = lambda loader, record: {'source_id': record.pk}
        source = CommonPoint
        mapping = {
            "latitude": "latitude",
            "longitude": "longitude",
            "name": "admin_level_1.name",
            "country_code": "admin_level_1.country_code",
        }


class ApplicationLoader(CommonLoader):
    def get_queryset(self):
        qs = ProjectApplication.objects.select_related(
            "eoi"
        ).prefetch_related(
            "focal_points",
        )
        return qs

    def get_focal_points(
            self,
            record: ProjectApplication,
            values: dict,
            **kwargs,
    ):
        data = []
        ret = []
        for member in record.focal_points.all():
            # member is AccountUser
            ret.append(
                "{0.last_name} {0.first_name} ({0.email}) {0.phone}".format(
                    member,
                )
            )
            data.append(dict(
                last_name=member.last_name,
                first_name=member.first_name,
                email=member.email,
                phone=member.phone,
            ))

        values['focal_points_data'] = data
        return ", ".join(ret)

    def get_specializations(
            self,
            record: ProjectApplication,
            values: dict,
            **kwargs,
    ):
        data = []
        ret = []
        if record.eoi:
            for specialization in record.eoi.specializations.all():
                # member is ProjectEoiSpecializations
                ret.append(
                    "{0.name} ({0.category})".format(
                        specialization.specialization,
                    )
                )
                data.append(dict(
                    name=specialization.specialization.name,
                    category=specialization.specialization.category,
                ))

        values['specializations_data'] = data
        return ", ".join(ret)


class Application(UNPPDataMartModel):
    type_of_call = models.CharField(max_length=254, null=True, blank=True)
    title = models.CharField(max_length=254, null=True, blank=True)
    agency = models.CharField(max_length=254, null=True, blank=True)
    created_by = models.CharField(max_length=512, blank=True, null=True)
    focal_points = models.TextField(blank=True, null=True)
    focal_points_data = JSONField(blank=True, null=True, default=dict)
    locations = models.ForeignKey(
        "Location",
        models.DO_NOTHING,
        blank=True,
        null=True,
    )
    agency_office = models.CharField(max_length=254, null=True, blank=True)
    cn_template = models.CharField(max_length=100, blank=True, null=True)
    specializations = models.TextField(blank=True, null=True)
    specializations_data = JSONField(blank=True, null=True, default=dict)
    description = models.TextField(blank=True, null=True)
    goal = models.TextField(blank=True, null=True)
    other_information = models.TextField(blank=True, null=True)
    estimated_start_date = models.DateField(blank=True, null=True)

    loader = ApplicationLoader()

    class Meta:
        app_label = 'unpp'

    class Options:
        depends = (Location,)
        key = lambda loader, record: {'source_id': record.pk}
        source = ProjectApplication
        mapping = {
            "type_of_call": "eoi.display_type",  # TODO get actual CFEI_TYPES value
            "title": "eoi.title",
            "agency": "agency.name",
            "created_by": "submitter.fullname",
            "focal_points": "-",
            "focal_points_data": "i",
            "location": Location,
            "agency_office": "eoi.agency_office.country",
            "cn_template": "eoi.cn_template",
            "specializations": "-",
            "specializations_data": "i",
            "description": "description",
            "goal": "goal",
            "other_information": "other_information",
            "start_date": "start_date",
        }
