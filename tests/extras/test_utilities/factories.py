import factory
from django.contrib.auth import models

from etools_datamart.apps.data.models import PMPIndicators, Intervention

# class GroupFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = models.Group
#         django_get_or_create = ('name',)
#
#
# class PartnerOrganizationFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = PartnersPartnerorganization
#         django_get_or_create = ('name',)
from unicef_rest_framework.models import UserAccessControl, Service


class PMPIndicatorFactory(factory.DjangoModelFactory):
    class Meta:
        model = PMPIndicators


class InterventionFactory(factory.DjangoModelFactory):
    metadata = {}

    class Meta:
        model = Intervention


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: "user%03d" % n)

    last_name = factory.Faker('last_name')
    first_name = factory.Faker('first_name')

    email = factory.Sequence(lambda n: "m%03d@mailinator.com" % n)
    password = '123'

    # is_active = True

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


class UserAccessControlFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserAccessControl
        django_get_or_create = ('user',)


class ServiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Service
        django_get_or_create = ('name',)
