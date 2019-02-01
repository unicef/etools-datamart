import datetime
import logging
import time
from inspect import isclass

from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.db import connections, models, transaction
from django.utils import timezone
from django.utils.functional import cached_property

import celery
from crashlog.middleware import process_exception
from redis.exceptions import LockError
from strategy_field.utils import fqn, get_attr

from etools_datamart.apps.data.exceptions import LoaderException
from etools_datamart.celery import app

loadeables = set()
locks = caches['lock']

logger = logging.getLogger(__name__)

CREATED = 'created'
UPDATED = 'updated'
UNCHANGED = 'unchanged'
DELETED = 'deleted'

RUN_UNKNOWN = 0
RUN_MANUAL = 1
RUN_COMMAND = 2
RUN_SCHEDULE = 3
RUN_QUEUED = 4
RUN_AS_REQUIREMENT = 5
RUN_TYPES = ((RUN_UNKNOWN, ""),
             (RUN_MANUAL, "Manual"),
             (RUN_COMMAND, "cli"),
             (RUN_SCHEDULE, "Celery"),
             (RUN_QUEUED, "Forced queue"),
             (RUN_AS_REQUIREMENT, "Required by task"),
             )


class EtlResult:
    __slots__ = [CREATED, UPDATED, UNCHANGED, DELETED, 'status', 'context', 'error', 'retry']

    def __init__(self, updated=0, created=0, unchanged=0, deleted=0,
                 status='SUCCESS', context=None, error=None, retry=False, **kwargs):
        self.created = created
        self.updated = updated
        self.unchanged = unchanged
        self.deleted = deleted
        self.retry = retry
        self.status = status
        self.error = error
        self.context = context or {}

    def __repr__(self):
        return repr(self.as_dict())

    def incr(self, counter):
        setattr(self, counter, getattr(self, counter) + 1)

    # def add(self, counter, value):
    #     setattr(self, counter, getattr(self, counter) + value)

    def as_dict(self):
        return {'created': self.created,
                'updated': self.updated,
                'unchanged': self.unchanged,
                'deleted': self.deleted,
                'status': self.status,
                'error': self.error}

    # def __add__(self, other):
    #     if isinstance(other, EtlResult):
    #         ret = EtlResult(created=self.created + other.created,
    #                         updated=self.updated + other.updated,
    #                         unchanged=self.unchanged + other.unchanged,
    #                         deleted=self.deleted + other.deleted,
    #                         context=self.context
    #                         )
    #         return ret
    #     raise ValueError(f"Cannot add EtlREsult with {other}")

    # def __eq__(self, other):
    #     if isinstance(other, EtlResult):
    #         other = other.as_dict()
    #
    #     if isinstance(other, dict):
    #         return (self.created == other['created'] and
    #                 self.updated == other['updated'] and
    #                 self.unchanged == other['unchanged'] and
    #                 self.deleted == other['deleted']
    #                 )
    #     return False


DEFAULT_KEY = lambda country, record: dict(country_name=country.name,
                                           schema_name=country.schema_name,
                                           source_id=record.pk)


class RequiredIsRunning(Exception):

    def __init__(self, req, *args: object) -> None:
        self.req = req

    def __str__(self):
        return "Required datased %s is still updating" % self.req


class RequiredIsMissing(Exception):

    def __init__(self, req, *args: object) -> None:
        self.req = req

    def __str__(self):
        return "Missing required datased %s" % self.req


class LoaderOptions:
    __attrs__ = ['mapping', 'celery', 'source', 'last_modify_field',
                 'queryset', 'key', 'locks', 'filters',
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
        self.filters = None
        self.last_modify_field = None

        if base:
            for attr in self.__attrs__:
                if hasattr(base, attr):
                    if isinstance(getattr(self, attr), (list, tuple)):
                        n = getattr(self, attr) + getattr(base, attr)
                        setattr(self, attr, n)
                    else:
                        setattr(self, attr, getattr(base, attr, getattr(self, attr)))

    def contribute_to_class(self, model, name):
        self.model = model
        setattr(model, name, self)
        if not self.lock_key:  # pragma: no branch
            self.lock_key = f"{fqn(model)}-lock"


class LoaderTask(celery.Task):
    default_retry_delay = 3 * 60

    def __init__(self, loader) -> None:
        self.loader = loader
        self.linked_model = loader.model
        self.name = "load_{0.app_label}_{0.model_name}".format(loader.model._meta)

    def run(self, *args, **kwargs):
        logger.debug(kwargs)
        try:
            return self.loader.load(run_type=RUN_SCHEDULE, check_requirements=True)
        except (RequiredIsRunning, RequiredIsMissing) as e:  # pragma: no cover
            self.retry(exc=e)


class Loader:
    def __init__(self) -> None:
        self.config = None
        self.tree_parents = []
        self.always_update = False
        self.seen = []

    def __repr__(self):
        return "<%sLoader>" % self.model._meta.object_name

    # @property
    # def model_name(self):
    #     return ".".join([self.model._meta.app_label, self.model._meta.model_name])

    def contribute_to_class(self, model, name):
        self.model = model
        self.config = model._etl_config
        del model._etl_config
        if not model._meta.abstract:
            loadeables.add("{0._meta.app_label}.{0._meta.model_name}".format(model))
        # if self.config.celery:
        self.task = LoaderTask(self)
        self.config.celery.tasks.register(self.task)

        setattr(model, name, self)

    def get_queryset(self, context):

        if self.config.queryset:
            ret = self.config.queryset()
        elif self.config.source:
            ret = self.config.source.objects.all()
        else:  # pragma: no cover
            raise ValueError("Option must define 'queryset' or 'source' attribute")

        return ret

    def filter_queryset(self, qs, context):
        use_delta = context['filter_last_modified'] and not context['is_empty']

        if self.config.filters:
            qs = qs.filter(**self.config.filters)
        if use_delta and (self.config.last_modify_field and self.last_run):
            logger.info("Loader {self}: use deltas")
            qs = qs.filter(**{f"{self.config.last_modify_field}__gte": self.last_run})
        return qs

    @property
    def last_run(self):
        last_run = self.etl_task.last_run
        # delta is not required as last_run is set at the beginning
        # here just for safety
        if last_run and self.etl_task.elapsed:
            delta = datetime.timedelta(seconds=self.etl_task.elapsed)
            return last_run - delta
        return None

    def is_running(self):
        return self.etl_task.status == 'RUNNING'

    def need_refresh(self, sender):
        if not self.etl_task.last_success:
            return True
        if self.etl_task.status != 'SUCCESS':
            return True

        if sender.etl_task.last_success:
            return self.etl_task.last_success.day < sender.etl_task.last_run.day
        return False

    def is_record_changed(self, record, values):
        other = type(record)(**values)
        # for field_name, field_value in values.items():
        for field_name in self.fields_to_compare:
            if getattr(record, field_name) != getattr(other, field_name):
                return True
        return False

    def process_record(self, filters, values, context):
        stdout = context['stdout']
        verbosity = context['verbosity']

        if stdout and verbosity > 2:  # pragma: no cover
            stdout.write('.')
            stdout.flush()

        try:
            record, created = self.model.objects.get_or_create(**filters,
                                                               defaults=values)
            if created:
                op = CREATED
            else:
                if self.always_update or self.is_record_changed(record, values):
                    op = UPDATED
                    record, created = self.model.objects.update_or_create(**filters,
                                                                          defaults=values)
                else:
                    op = UNCHANGED
            self.seen.append(record.pk)
            return op
        except Exception as e:  # pragma: no cover
            logger.exception(e)
            err = process_exception(e)
            raise LoaderException(f"Error in {self}: {e}",
                                  err) from e

    def get_values(self, country, record, context):
        ret = {'area_code': country.business_area_code,
               'schema_name': country.schema_name,
               'country_name': country.name,
               'source_id': record.id
               }
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
                except AttributeError:  # pragma: no cover
                    pass
            elif callable(v):
                ret[k] = v(country, record)
            else:
                ret[k] = get_attr(record, v)
        ret['seen'] = context['today']
        return ret

    def post_process_country(self, country, context):
        for mart, etools in self.tree_parents:
            kk = self.model.objects.get(schema_name=country.schema_name,
                                        source_id=mart)
            kk.parent = self.model.objects.get(schema_name=country.schema_name,
                                               source_id=etools)
            kk.save()
        self.tree_parents = []

        # mark seen records
        self.model.objects.filter(id__in=self.seen).update(seen=context['today'])

    def process_country(self, country, context):
        qs = self.filter_queryset(self.get_queryset(context), context)
        max_records = context['max_records']
        self.seen = []
        for record in qs.all():
            filters = self.config.key(country, record)
            values = self.get_values(country, record, context)
            op = self.process_record(filters, values, context)
            self.results.incr(op)
            context['records'] += 1
            if max_records and context['records'] >= max_records:
                break

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

    @cached_property
    def etl_task(self):
        from etools_datamart.apps.etl.models import EtlTask
        return EtlTask.objects.get_or_create(task=self.task.name,
                                             content_type=ContentType.objects.get_for_model(self.config.model),
                                             table_name=self.config.model._meta.db_table)[0]

    def on_start(self, run_type):
        from django.utils import timezone
        logger.info(f"Start loader {self}")
        self._start = time.time()

        defs = {'status': 'RUNNING',
                'elapsed': None,
                'run_type': run_type,
                'last_run': timezone.now()}
        self.etl_task.update(**defs)

    def on_end(self, error=None, retry=False):
        from etools_datamart.apps.subscriptions.models import Subscription
        from django.utils import timezone

        cost = time.time() - self._start
        defs = {'elapsed': cost,
                'results': self.results.as_dict()}
        if retry:
            defs['status'] = 'RETRY'
            defs['results'] = str(error)
            defs['last_failure'] = timezone.now()
        elif error:
            defs['status'] = 'FAILURE'
            defs['results'] = str(error)
            defs['last_failure'] = timezone.now()
        else:
            defs['status'] = 'SUCCESS'
            if self.results.error:
                defs['status'] = 'ERROR'
                defs['last_failure'] = timezone.now()
            else:
                defs['last_success'] = timezone.now()
                defs['last_failure'] = None
                if self.results.created > 0 or self.results.updated > 0:
                    defs['last_changes'] = timezone.now()
                    for service in self.config.model.linked_services:
                        service.invalidate_cache()
                        Subscription.objects.notify(self.config.model)
        self.etl_task.update(**defs)

    def lock(self):
        lock = locks.lock(self.config.lock_key, timeout=self.config.timeout)
        if lock.acquire(blocking=False):
            return lock

    def load(self, *, verbosity=0, always_update=False, stdout=None,
             ignore_dependencies=False, max_records=None, countries=None,
             ignore_last_modify_field=False, run_type=RUN_UNKNOWN,
             check_requirements=False, force_requirements=False):
        self.on_start(run_type)
        self.results = EtlResult()
        logger.debug(f"Running loader {self}")
        lock = self.lock()
        try:
            if lock:  # pragma: no branch
                if not ignore_dependencies:
                    for requirement in self.config.depends:
                        if force_requirements or requirement.loader.need_refresh(self):
                            if check_requirements:
                                raise RequiredIsMissing(requirement)
                            logger.info(f"Loader {requirement} need refresh")
                            if requirement.loader.is_running():
                                raise RequiredIsRunning(requirement)
                            logger.info(f"Load required dataset {requirement}")
                            requirement.loader.load(stdout=stdout,
                                                    force_requirements=force_requirements,
                                                    check_requirements=check_requirements,
                                                    run_type=RUN_AS_REQUIREMENT)
                        else:
                            logger.info(f"Loader {requirement} is uptodate")
                self.always_update = always_update
                connection = connections['etools']
                if countries is None:  # pragma: no branch
                    countries = connection.get_tenants()
                self.mapping = {}
                mart_fields = self.model._meta.concrete_fields
                for field in mart_fields:
                    if field.name not in ['country_name', 'schema_name', 'area_code', 'source_id',
                                          'id', 'last_modify_date']:
                        self.mapping[field.name] = field.name
                if self.config.mapping:  # pragma: no branch
                    self.mapping.update(self.config.mapping)
                today = timezone.now()
                context = self.get_context(today=today,
                                           countries=countries,
                                           max_records=max_records,
                                           verbosity=verbosity,
                                           records=0,
                                           filter_last_modified=not ignore_last_modify_field,
                                           is_empty=not self.model.objects.exists(),
                                           stdout=stdout)
                sid = transaction.savepoint()
                total_countries = len(countries)
                try:
                    self.results.context = context
                    self.fields_to_compare = [f for f in self.mapping.keys() if f not in ["seen"]]

                    for i, country in enumerate(countries, 1):
                        if stdout and verbosity > 0:
                            stdout.write(f"{i:>3}/{total_countries} {country}")
                        connection.set_schemas([country.schema_name])
                        self.process_country(country, context)
                        self.post_process_country(country, context)
                        if max_records and context['records'] >= max_records:
                            break
                    if stdout and verbosity > 0:
                        stdout.write("\n")
                    deleted = self.model.objects.exclude(seen=today).delete()[0]
                    self.results.deleted = deleted
                except Exception:
                    transaction.savepoint_rollback(sid)
                    raise
            else:
                logger.info(f"Unable to get lock for {self}")

        except (RequiredIsMissing, RequiredIsRunning) as e:
            self.on_end(error=e, retry=True)
            raise
        except BaseException as e:
            self.on_end(e)
            process_exception(e)
            raise
        else:
            self.on_end(None)
        finally:
            if lock:  # pragma: no branch
                try:
                    lock.release()
                except LockError as e:  # pragma: no cover
                    logger.warning(e)

        return self.results
