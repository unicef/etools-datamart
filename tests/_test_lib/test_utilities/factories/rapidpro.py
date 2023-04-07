from test_utilities.factories import factory, RegisterModelFactory

from etools_datamart.apps.mart.rapidpro import models


class EToolsModelFactory(RegisterModelFactory):
    pass


class RGroupFactory(RegisterModelFactory):
    name = factory.Sequence(lambda n: "name%03d" % n)

    class Meta:
        model = models.Group
        django_get_or_create = ("name",)
