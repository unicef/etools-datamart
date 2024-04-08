from django.contrib.auth.models import AbstractUser
from django.db import connections
from django.db.models import QuerySet
from django.db.models.manager import BaseManager

from unicef_security.models import SecurityMixin


class User(AbstractUser, SecurityMixin):
    pass


class DataMartQuerySet(QuerySet):
    def get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except self.model.DoesNotExist as e:
            raise self.model.DoesNotExist("%s  (%s %s)" % (e, args, kwargs))
        except self.model.MultipleObjectsReturned as e:  # pragma: no cover
            raise self.model.MultipleObjectsReturned("%s (%s %s) " % (e, args, kwargs))

    def filter_schemas(self, *schemas):
        if schemas and schemas[0]:
            return self.filter(schema_name__in=schemas)
        return self


class DataMartManager(BaseManager.from_queryset(DataMartQuerySet)):
    def truncate(self, reset=True):
        if reset:
            restart = "RESTART IDENTITY"
        else:
            restart = ""
        with connections["default"].cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" {1} CASCADE;'.format(self.model._meta.db_table, restart))
