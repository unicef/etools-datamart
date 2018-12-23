
from django.contrib.auth.models import Group
from django.utils import timezone

import factory
from factory import SubFactory
from factory.base import FactoryMetaClass
from post_office.models import EmailTemplate

import unicef_rest_framework.models
import unicef_security.models

from etools_datamart.apps.security.models import SchemaAccessControl
from etools_datamart.apps.subscriptions.models import Subscription
from etools_datamart.apps.tracking.models import APIRequestLog

today = timezone.now()

factories_registry = {}


class AutoRegisterFactoryMetaClass(FactoryMetaClass):
    def __new__(mcs, class_name, bases, attrs):
        new_class = super().__new__(mcs, class_name, bases, attrs)
        factories_registry[new_class._meta.model] = new_class
        return new_class


class RegisterModelFactory(factory.DjangoModelFactory, metaclass=AutoRegisterFactoryMetaClass):
    pass


# class TaskLogFactory(RegisterModelFactory):
#     elapsed = 10
#     last_success = timezone.now()
#     last_failure = timezone.now()
#     last_changes = timezone.now()
#
#     class Meta:
#         model = EtlTask


class APIRequestLogFactory(RegisterModelFactory):
    requested_at = timezone.now()
    remote_addr = factory.Faker('ipv4_public')

    class Meta:
        model = APIRequestLog


class ServiceFactory(RegisterModelFactory):
    class Meta:
        model = unicef_rest_framework.models.Service
        django_get_or_create = ('viewset',)


class GroupFactory(RegisterModelFactory):
    name = factory.Sequence(lambda n: "name%03d" % n)

    class Meta:
        model = Group
        django_get_or_create = ('name',)


class UserFactory(RegisterModelFactory):
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
        from ..perms import user_grant_permissions

        permissions = kwargs.pop('permissions', [])

        password = kwargs.pop('password')
        user = super()._prepare(cls, create, **kwargs)
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


class UserAccessControlFactory(RegisterModelFactory):
    policy = unicef_rest_framework.models.UserAccessControl.POLICY_ALLOW
    serializers = ["std"]

    class Meta:
        model = unicef_rest_framework.models.UserAccessControl
        django_get_or_create = ('user', 'service')


class SystemFilterFactory(RegisterModelFactory):
    class Meta:
        model = unicef_rest_framework.models.SystemFilter
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


class SubscriptionFactory(RegisterModelFactory):
    kwargs = ''
    user = SubFactory(UserFactory)
    type = Subscription.MESSAGE

    # content_type = lambda x: ContentType.objects.get_for_model(HACT)  # noqa: E731

    class Meta:
        model = Subscription
        django_get_or_create = ('user', 'content_type')


class EmailTemplateFactory(RegisterModelFactory):
    name = 'dataset_changed'

    class Meta:
        model = EmailTemplate
        django_get_or_create = ('name',)


class RegionFactory(RegisterModelFactory):
    code = factory.Sequence(lambda n: "code%03d" % n)
    name = factory.Sequence(lambda n: "name%03d" % n)

    class Meta:
        model = unicef_security.models.Region
        django_get_or_create = ('name',)


class SchemaAccessControlFactory(RegisterModelFactory):
    group = factory.SubFactory(GroupFactory)
    schemas = ['bolivia', 'chad']

    class Meta:
        model = SchemaAccessControl


class BusinessAreaFactory(RegisterModelFactory):
    code = factory.Sequence(lambda n: "code%03d" % n)
    region = SubFactory(RegionFactory)

    class Meta:
        model = unicef_security.models.BusinessArea
        django_get_or_create = ('name',)
