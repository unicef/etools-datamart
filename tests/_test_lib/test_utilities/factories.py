import random
from datetime import datetime

import factory
import unicef_security.models
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db import connections
from django.utils import timezone
from factory import SubFactory
from post_office.models import EmailTemplate
from unicef_rest_framework.models import Service, SystemFilter, UserAccessControl

from etools_datamart.apps.data.models import FAMIndicator, HACT, Intervention, PMPIndicators, UserStats
from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.apps.subscriptions.models import Subscription
from etools_datamart.apps.tracking.models import APIRequestLog

today = timezone.now()


class TaskLogFactory(factory.DjangoModelFactory):
    elapsed = 10
    last_success = timezone.now()
    last_failure = timezone.now()
    last_changes = timezone.now()

    class Meta:
        model = EtlTask


class APIRequestLogFactory(factory.DjangoModelFactory):
    requested_at = timezone.now()
    remote_addr = factory.Faker('ipv4_public')

    class Meta:
        model = APIRequestLog


class HACTFactory(factory.DjangoModelFactory):
    year = today.year
    country_name = lambda: random.choice(connections['etools'].get_tenants())  # noqa

    class Meta:
        model = HACT


class PMPIndicatorFactory(factory.DjangoModelFactory):
    # country_name = lambda: random.choice(connections['etools'].get_tenants())  # noqa
    class Meta:
        model = PMPIndicators


class FAMIndicatorFactory(factory.DjangoModelFactory):
    month = today
    last_modify_date = timezone.now()

    class Meta:
        model = FAMIndicator


class ServiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Service
        django_get_or_create = ('viewset',)


class InterventionFactory(factory.DjangoModelFactory):
    metadata = {}
    title = factory.Sequence(lambda n: "title%03d" % n)
    number = factory.Sequence(lambda n: "#%03d" % n)

    class Meta:
        model = Intervention


class GroupFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "name%03d" % n)

    class Meta:
        model = Group
        django_get_or_create = ('name',)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = unicef_security.models.User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: "user%03d" % n)

    last_name = factory.Faker('last_name')
    first_name = factory.Faker('first_name')

    email = factory.Sequence(lambda n: "m%03d@mailinator.com" % n)
    password = 'password'
    is_superuser = False
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        from .perms import user_grant_permissions

        permissions = kwargs.pop('permissions', [])

        password = kwargs.pop('password')
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        user_grant_permissions(user, permissions).start()
        return user


class AdminFactory(UserFactory):
    is_superuser = True


class AnonUserFactory(UserFactory):
    username = 'anonymous'


class UserAccessControlFactory(factory.DjangoModelFactory):
    policy = UserAccessControl.POLICY_ALLOW
    serializers = ["std"]

    class Meta:
        model = UserAccessControl
        django_get_or_create = ('user', 'service')


class UserStatsFactory(factory.DjangoModelFactory):
    month = lambda: datetime(today.year, random.choice([1, 2, 3]), 1)  # noqa
    country_name = lambda: random.choice(connections['etools'].get_tenants())  # noqa

    class Meta:
        model = UserStats
        django_get_or_create = ('month', 'country_name')


class SystemFilterFactory(factory.DjangoModelFactory):
    class Meta:
        model = SystemFilter
        django_get_or_create = ('user', 'service')

    @factory.post_generation
    def rules(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # if isinstance(extracted, dict):
            for field, value in extracted.items():
                rule = self.rules.create(field=field, value=value)
                rule.save()


class SubscriptionFactory(factory.DjangoModelFactory):
    kwargs = ''
    user = SubFactory(UserFactory)
    type = Subscription.MESSAGE
    content_type = lambda x: ContentType.objects.get_for_model(HACT)  # noqa: E731

    class Meta:
        model = Subscription
        django_get_or_create = ('user', 'content_type')


class EmailTemplateFactory(factory.DjangoModelFactory):
    name = 'dataset_changed'

    class Meta:
        model = EmailTemplate
        django_get_or_create = ('name',)


class RegionFactory(factory.DjangoModelFactory):
    code = factory.Sequence(lambda n: "code%03d" % n)
    name = factory.Sequence(lambda n: "name%03d" % n)

    class Meta:
        model = unicef_security.models.Region
        django_get_or_create = ('name',)


class BusinessAreaFactory(factory.DjangoModelFactory):
    code = factory.Sequence(lambda n: "code%03d" % n)
    region = SubFactory(RegionFactory)

    class Meta:
        model = unicef_security.models.BusinessArea
        django_get_or_create = ('name',)


# class RoleFactory(factory.DjangoModelFactory):
#     user = SubFactory(UserFactory)
#     group = SubFactory(GroupFactory)
#     business_area = SubFactory(BusinessAreaFactory)
#
#     class Meta:
#         model = unicef_security.models.Role
#         django_get_or_create = ('user', 'group', 'business_area')
