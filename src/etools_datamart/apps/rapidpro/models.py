from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from celery.local import class_property
from constance import config
from sentry_sdk import capture_exception

from etools_datamart.apps.data.models.base import DataMartManager
from etools_datamart.apps.etl.base import DataMartModelBase
from etools_datamart.apps.rapidpro.loader import TembaLoader, TembaLoaderOptions


class RapidProModelBase(DataMartModelBase):
    loader_option_class = TembaLoaderOptions
    loader_class = TembaLoader


class Source(models.Model):
    name = models.CharField(max_length=100)
    api_token = models.CharField(max_length=40)
    server = models.CharField(max_length=100, default=config.RAPIDPRO_ADDRESS)
    is_active = models.BooleanField(default=False)

    class Meta:
        app_label = 'rapidpro'

    def __str__(self):
        return self.name


class Organization(models.Model):
    {
        "uuid": "6a44ca78-a4c2-4862-a7d3-2932f9b3a7c3",
        "name": "Nyaruka",
        "country": "RW",
        "languages": ["eng", "fra"],
        "primary_language": "eng",
        "timezone": "Africa/Kigali",
        "date_style": "day_first",
        "credits": {"used": 121433, "remaining": 3452},
        "anon": False
    }
    source = models.OneToOneField(Source, on_delete=models.CASCADE,
                                  blank=True, null=True)
    # uuid = models.UUIDField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    primary_language = models.CharField(max_length=100, null=True, blank=True)
    languages = ArrayField(models.CharField(max_length=100))
    timezone = models.CharField(max_length=100, null=True, blank=True)
    date_style = models.CharField(max_length=100, null=True, blank=True)
    credits = JSONField(default=dict)
    anon = models.BooleanField(default=False)

    objects = DataMartManager()

    # loader = TembaLoader()
    class Meta:
        app_label = 'rapidpro'

    class Options:
        source = 'https://app.rapidpro.io/api/v2/org'

    def __str__(self):
        return self.name


class RapidProManager(DataMartManager):
    pass


class RapidProDataMartModel(models.Model, metaclass=RapidProModelBase):
    source_id = models.CharField(max_length=100, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    objects = RapidProManager()

    class Meta:
        abstract = True

    @class_property
    def service(self):
        from unicef_rest_framework.models import Service
        return Service.objects.get(source_model=ContentType.objects.get_for_model(self))

    @class_property
    def linked_services(self):
        from unicef_rest_framework.models import Service
        return [s for s in Service.objects.all() if s.managed_model == self]


class Group(RapidProDataMartModel):
    uuid = models.UUIDField(unique=True, db_index=True, null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    query = models.TextField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.organization)

    class Options:
        source = 'groups'


class ContactLoader(TembaLoader):

    def get_groups(self, record, ret, field_name):
        return [oo.serialize() for oo in record.groups]


class Contact(RapidProDataMartModel):
    uuid = models.UUIDField(unique=True, db_index=True, null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    urns = ArrayField(
        models.CharField(max_length=100),
        default=list,
        null=True, blank=True
    )
    # groups = models.ManyToManyField(Group)
    groups = JSONField(default=dict, null=True, blank=True)
    fields = JSONField(default=dict, null=True, blank=True)
    blocked = models.BooleanField(null=True, blank=True)
    stopped = models.BooleanField(null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    loader = ContactLoader()

    def __str__(self):
        return '{} ({})'.format(self.name, self.organization)

    class Options:
        source = 'contacts'
        exclude_from_compare = ['groups', ]
        fields_to_compare = None


class CampaignLoader(TembaLoader):
    def get_group(self, record, values, field_name):
        return self.get_foreign_key(Group, record.group)


class Campaign(RapidProDataMartModel):
    uuid = models.UUIDField(unique=True, db_index=True)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=100)
    loader = CampaignLoader()

    class Options:
        source = 'campaigns'

    def __str__(self):
        return '{} ({})'.format(self.name, self.organization)


class Label(RapidProDataMartModel):
    uuid = models.UUIDField(unique=True, db_index=True)
    name = models.CharField(max_length=100)
    count = models.IntegerField(null=True, blank=True)

    class Options:
        source = 'labels'

    def __str__(self):
        return '{} ({})'.format(self.name, self.organization)


class Runs(RapidProDataMartModel):
    active = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)
    expired = models.IntegerField(default=0)
    interrupted = models.IntegerField(default=0)

    class Options:
        source = 'runs'

    def __str__(self):
        return f'{self.active} {self.completed} {self.expired} {self.interrupted}'


class FlowLoader(TembaLoader):
    def get_runs(self, record, values, field_name):
        return record.runs.serialize()

    def process_record(self, filters, values):
        runs = values.pop('runs')
        op = super().process_record(filters, values)
        runs['organization'] = self.record.organization
        rr, __ = Runs.objects.update_or_create(id=self.record.id,
                                               defaults=runs)
        self.record.runs = rr
        self.record.save()
        for label in self.source_record.labels:
            try:
                lbl = self.get_foreign_key(Label, label)
                self.record.labels.add(lbl)
            except Label.DoesNotExist as e:
                capture_exception(e)

        return op


class Flow(RapidProDataMartModel):
    uuid = models.UUIDField(unique=True, db_index=True)
    name = models.CharField(max_length=100)
    archived = models.BooleanField(default=False)
    labels = models.ManyToManyField(Label)
    expires = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    runs = models.OneToOneField(Runs, null=True, blank=True, on_delete=models.CASCADE)

    loader = FlowLoader()

    class Options:
        source = 'flows'

    def __str__(self):
        return '{} ({})'.format(self.name, self.organization)


class FlowStartLoader(TembaLoader):
    def process_record(self, filters, values):
        op = super().process_record(filters, values)
        for m2m_name in ('groups', 'contacts'):
            m2m = getattr(self.source_record, m2m_name)
            m2m_local = getattr(self.record, m2m_name)
            m2m_local_model = m2m_local.model
            for entry in m2m:
                try:
                    lbl = self.get_foreign_key(m2m_local_model, entry)
                    m2m_local.add(lbl)
                except ObjectDoesNotExist as e:
                    capture_exception(e)

        return op


class FlowStart(RapidProDataMartModel):
    uuid = models.UUIDField(unique=True, db_index=True)
    flow = models.ForeignKey(Flow, null=True, blank=True, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)
    contacts = models.ManyToManyField(Contact)
    restart_participants = models.NullBooleanField()
    status = models.CharField(max_length=100)
    extra = JSONField(default=dict)
    created_on = models.DateTimeField(null=True, blank=True)
    modified_on = models.DateTimeField(null=True, blank=True)

    loader = FlowStartLoader()

    class Options:
        source = 'flow_starts'
        depends = (Flow, Group, Contact)
