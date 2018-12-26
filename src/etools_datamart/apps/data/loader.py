import logging
from inspect import isclass

from django.core.cache import caches
from django.db import connections, models
from django.utils import timezone

import celery
from crashlog.middleware import process_exception
from redis.exceptions import LockError
from strategy_field.utils import fqn, get_attr

from etools_datamart.celery import app

loadeables = set()
locks = caches['lock']

logger = logging.getLogger(__name__)

CREATED = 'created'
UPDATED = 'updated'
UNCHANGED = 'unchanged'


class EtlResult:
    __slots__ = [CREATED, UPDATED, UNCHANGED]

    def __init__(self, updated=0, created=0, unchanged=0, **kwargs):
        self.created = created
        self.updated = updated
        self.unchanged = unchanged

    def __repr__(self):
        return repr(self.as_dict())

    def incr(self, counter):
        setattr(self, counter, getattr(self, counter) + 1)

    def as_dict(self):
        return {'created': self.created,
                'updated': self.updated,
                'unchanged': self.unchanged}

    def __eq__(self, other):
        if isinstance(other, EtlResult):
            other = other.as_dict()

        if isinstance(other, dict):
            return (self.created == other['created'] and
                    self.updated == other['updated'] and
                    self.unchanged == other['unchanged'])
        return False


def is_record_changed(record, values):
    other = type(record)(**values)
    for field_name, field_value in values.items():
        if getattr(record, field_name) != getattr(other, field_name):
            return True
    return False


DEFAULT_KEY = lambda country, record: dict(country_name=country.name,
                                           schema_name=country.schema_name,
                                           source_id=record.pk)


class LoaderOptions:
    __attrs__ = ['mapping', 'celery', 'source',
                 'queryset', 'key', 'locks',
                 'depends', 'timeout', 'lock_key']

    def __init__(self, base=None):
        self.mapping = {}
        self.celery = app
        self.queryset = None
        self.source = None
        self.lock_key = None
        self.key = DEFAULT_KEY
        self.timeout = None
        self.depends = ()
        if base:
            for attr in self.__attrs__:
                if hasattr(base, attr):
                    if isinstance(getattr(self, attr), (list, tuple)):
                        n = getattr(self, attr) + getattr(base, attr)
                        setattr(self, attr, n)
                    else:
                        setattr(self, attr, getattr(base, attr, getattr(self, attr)))

        if not self.queryset and self.source:
            self.queryset = lambda: self.source.objects

    def contribute_to_class(self, model, name):
        self.model = model
        setattr(model, name, self)
        if not self.lock_key:
            self.lock_key = f"{fqn(model)}-lock"


class LoaderTask(celery.Task):

    def __init__(self, loader) -> None:
        self.loader = loader
        self.linked_model = loader.model
        # self.name = fqn(self.linked_model)
        self.name = "load_{0.app_label}_{0.model_name}".format(loader.model._meta)

    def run(self, *args, **kwargs):
        return self.loader.load()


# def get_or_fail(Model, **kwargs):
#     try:
#         Model.objects.get(**kwargs)
#     except Model.DoesNotExist:
#         raise Model.DoesNotExist(f"Unable to get {Model.__name__} using {kwargs}")


class Loader:
    # __slots__ = ['model', 'config', 'mapping', 'task', 'tree_parents', 'always_update']

    def __init__(self) -> None:
        self.config = None
        self.tree_parents = []
        self.always_update = False

    def __repr__(self):
        return "<%sLoader>" % self.model._meta.object_name

    def contribute_to_class(self, model, name):
        self.model = model
        self.config = model._etl_config
        del model._etl_config
        if not model._meta.abstract:
            loadeables.add("{0._meta.app_label}.{0._meta.model_name}".format(model))
        if self.config.celery:
            self.task = LoaderTask(self)
            self.config.celery.tasks.register(self.task)

        setattr(model, name, self)

    # def deconstruct(self):
    #     return []
    #
    # def check(self, **kwargs):
    #     return []

    def process(self, filters, values):
        try:
            existing, created = self.model.objects.get_or_create(**filters,
                                                                 defaults=values)
            if created:
                op = CREATED
            else:
                if self.always_update or is_record_changed(existing, values):
                    op = UPDATED
                    self.model.objects.update_or_create(**filters,
                                                        defaults=values)
                else:
                    op = UNCHANGED
            return op
        except Exception as e:  # pragma: no cover
            logger.exception(e)
            process_exception(e)
            raise Exception(f"Error in {self}: {e}") from e

    def get_values(self, country, record):
        ret = {}
        for k, v in self.mapping.items():
            if v == '__self__':
                try:
                    ret[k] = self.model.objects.get(schema_name=country.schema_name,
                                                    source_id=getattr(record, k).id)
                except AttributeError:
                    ret[k] = None
                except self.model.DoesNotExist:
                    ret[k] = None
                    self.tree_parents.append((record.id, getattr(record, k).id))

            elif isclass(v) and issubclass(v, models.Model):
                try:
                    ret[k] = v.objects.get(schema_name=country.schema_name,
                                           source_id=getattr(record, k).id)
                except AttributeError:
                    pass
            elif callable(v):
                ret[k] = v(country, record)
            else:
                ret[k] = get_attr(record, v)
        return ret

    def process_post_country(self, country, context):
        for mart, etools in self.tree_parents:
            kk = self.model.objects.get(schema_name=country.schema_name,
                                        source_id=mart)
            kk.parent = self.model.objects.get(schema_name=country.schema_name,
                                               source_id=etools)
            kk.save()
        self.tree_parents = []

    def process_country(self, results: EtlResult, country, context) -> EtlResult:
        qs = self.config.queryset()
        stdout = context['stdout']
        max_records = context['max_records']
        for record in qs.all():
            filters = self.config.key(country, record)
            values = self.get_values(country, record)
            op = self.process(filters, values)
            results.incr(op)
            context['records'] += 1
            if stdout:  # pragma: no cover
                stdout.write('.')
                stdout.flush()
            if max_records and context['records'] >= max_records:
                break
        return results

    def get_context(self, **kwargs):
        context = {}
        context.update(kwargs)
        return context

    @property
    def is_locked(self):
        return self.config.lock_key in locks

    def unlock(self):
        try:
            lock = locks.lock(self.config.lock_key, timeout=self.config.timeout)
            locks.delete(self.config.lock_key)
            lock.release()
        except LockError:
            pass

    def load(self, verbosity=0, always_update=False, stdout=None,
             ignore_dependencies=False, max_records=None, countries=None):
        have_lock = False
        results = EtlResult()
        lock = locks.lock(self.config.lock_key, timeout=self.config.timeout)
        try:
            have_lock = lock.acquire(blocking=False)
            if have_lock:  # pragma: no branch
                if not ignore_dependencies:
                    for dependency in self.config.depends:
                        dependency.loader.load(stdout=stdout)
                self.always_update = always_update
                connection = connections['etools']
                if not countries:  # pragma: no branch
                    countries = connection.get_tenants()
                if self.config.mapping:
                    self.mapping = {}
                    mart_fields = self.model._meta.concrete_fields
                    for field in mart_fields:
                        if field.name not in ['country_name', 'schema_name', 'area_code',
                                              'id', 'last_modify_date']:
                            self.mapping[field.name] = field.name
                    self.mapping.update(self.config.mapping)

                context = self.get_context(today=timezone.now(),
                                           countries=countries,
                                           max_records=max_records,
                                           records=0,
                                           stdout=stdout)

                for country in countries:
                    if stdout:  # pragma: no cover
                        stdout.write(f"{country}\n")
                    connection.set_schemas([country.schema_name])
                    self.process_country(results, country, context)
                    self.process_post_country(country, context)
                    if max_records and context['records'] >= max_records:
                        break
                    if stdout:  # pragma: no cover
                        stdout.write("\n")
        finally:
            if have_lock:  # pragma: no branch
                try:
                    lock.release()
                except LockError as e:  # pragma: no cover
                    logger.warning(e)
        return results
