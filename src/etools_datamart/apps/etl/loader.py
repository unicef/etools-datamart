import json
import time
from uuid import UUID

from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.utils import timezone
from django.utils.functional import cached_property

import celery
from celery.utils.log import get_task_logger
from constance import config
from crashlog.middleware import process_exception
from redis.exceptions import LockError
from strategy_field.utils import fqn, get_attr

from etools_datamart.apps.etl.exceptions import (LoaderException, MaxRecordsException,
                                                 RequiredIsMissing, RequiredIsRunning,)
from etools_datamart.celery import app

loadeables = set()
locks = caches['lock']
cache = caches['default']

# logger = logging.getLogger(__name__)
logger = get_task_logger(__name__)

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
    __slots__ = [CREATED, UPDATED, UNCHANGED, DELETED, 'processed', 'total_records',
                 'status', 'context', 'error', 'retry']

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
        self.processed = 0
        self.total_records = 0

    def __repr__(self):
        return repr(self.as_dict())

    def incr(self, counter):
        setattr(self, counter, getattr(self, counter) + 1)
        self.processed += 1

    # def add(self, counter, value):
    #     setattr(self, counter, getattr(self, counter) + value)

    def as_dict(self):
        return {'created': self.created,
                'updated': self.updated,
                'unchanged': self.unchanged,
                'deleted': self.deleted,
                'status': self.status,
                'error': self.error,
                'processed': self.processed,
                'total_records': self.total_records}


undefined = object()


class BaseLoaderOptions:
    DEFAULT_KEY = lambda loader, record: dict(source_id=record.pk)
    __attrs__ = ['mapping', 'celery', 'source', 'last_modify_field',
                 'queryset', 'key', 'locks', 'filters', 'sync_deleted_records', 'truncate',
                 'depends', 'timeout', 'lock_key', 'always_update', 'fields_to_compare',
                 'exclude_from_compare']

    def __init__(self, base=None):
        self.mapping = {}
        self.host = config.RAPIDPRO_ADDRESS
        self.celery = app
        self.source = None
        self.queryset = None
        self.always_update = False
        self.source = None
        self.lock_key = None
        self.key = undefined
        self.timeout = None
        self.depends = ()
        self.filters = None
        self.last_modify_field = None
        self.sync_deleted_records = lambda loader: True
        self.truncate = False
        self.fields_to_compare = None
        self.exclude_from_compare = ['seen']

        if base:
            for attr in self.__attrs__:
                if hasattr(base, attr):
                    if isinstance(getattr(self, attr), (list, tuple)):
                        n = getattr(self, attr) + getattr(base, attr)
                    else:
                        n = getattr(base, attr, getattr(self, attr))
                    setattr(self, attr, n)

        if self.key == undefined:
            self.key = type(self).DEFAULT_KEY

        if self.truncate:
            self.sync_deleted_records = lambda loader: False

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
            if self.loader.etl_task.task_id:
                return EtlResult()
            kwargs.setdefault('ignore_dependencies', False)
            kwargs.setdefault('force_requirements', True)
            return self.loader.load(**kwargs)
        except (RequiredIsRunning, RequiredIsMissing) as e:  # pragma: no cover
            st = f'RETRY {self.request.retries}/{config.ETL_MAX_RETRIES}'
            self.loader.etl_task.status = st
            self.loader.etl_task.save()
            raise self.retry(exc=e, max_retries=config.ETL_MAX_RETRIES,
                             countdown=config.ETL_RETRY_COUNTDOWN)
        except Exception as e:  # pragma: no cover
            # self.loader.etl_task.status = 'ERROR'
            # self.loader.etl_task.save()
            process_exception(e)
            raise


def _compare_json(dict1, dict2):
    return json.dumps(dict1, sort_keys=True, indent=0) == json.dumps(dict2, sort_keys=True, indent=0)


def equal(current, new_value):
    if isinstance(current, (dict, list, tuple)):
        return _compare_json(current, new_value)
    elif isinstance(current, UUID):
        return current == UUID(new_value)
    elif isinstance(new_value, bool):
        return str(current) == str(new_value)
    return current == new_value


def has_attr(obj, attr):
    """Recursive get object's attribute. May use dot notation."""
    none = object()
    if '.' not in attr:
        ret = getattr(obj, attr, none)
    else:
        L = attr.split('.')
        ret = has_attr(getattr(obj, L[0], none), '.'.join(L[1:]))
    return ret != none


class BaseLoader:
    noop = object()

    def __init__(self) -> None:
        self.config = None
        self.context = {}
        self.tree_parents = []
        self.fields_to_compare = None

    def __repr__(self):
        return "<%sLoader>" % self.model._meta.object_name

    def __str__(self):
        return "%sLoader" % self.model._meta.object_name

    # @property
    # def model_name(self):
    #     return ".".join([self.model._meta.app_label, self.model._meta.model_name])

    def contribute_to_class(self, model, name):
        self.model = model
        if not model._meta.abstract:
            loadeables.add("{0._meta.app_label}.{0._meta.model_name}".format(model))
            self.config = model._etl_config
            del model._etl_config
            self.task = LoaderTask(self)
            self.config.celery.tasks.register(self.task)

        setattr(model, name, self)

    @property
    def last_run(self):
        # last_run = self.etl_task.last_run
        # delta is not required as last_run is set at the beginning
        # here just for safety
        # if last_run and self.etl_task.elapsed:
        #     delta = datetime.timedelta(seconds=self.etl_task.elapsed)
        #     return last_run - delta
        return self.etl_task.last_run

    def is_running(self):
        return self.etl_task.status == 'RUNNING'

    def need_refresh(self, other):
        if not self.etl_task.last_success or self.etl_task.status != 'SUCCESS':
            logger.info('%s: Refresh needed due no successfully run' % self)
            return True
        if self.etl_task.last_success.date() < timezone.now().date():
            logger.info('%s: Refresh needed because last success too old' % self)
            return True
        else:
            pass
        return False

    def is_record_changed(self, record, values):
        other = type(record)(**values)
        for field_name in self.fields_to_compare:
            new = getattr(other, field_name)
            current = getattr(record, field_name)

            if not equal(current, new):
                verbosity = self.context['verbosity']
                if verbosity >= 2:  # pragma: no cover
                    stdout = self.context['stdout']
                    stdout.write("Detected field changed '%s': current: %s(%s) new value: %s(%s)\n" %
                                 (field_name,
                                  getattr(record, field_name),
                                  type(getattr(record, field_name)),
                                  getattr(other, field_name),
                                  type(getattr(other, field_name))
                                  ))
                    stdout.flush()

                return True
        return False

    def process_record(self, filters, values):
        stdout = self.context['stdout']
        verbosity = self.context['verbosity']
        if stdout and verbosity > 2:  # pragma: no cover
            stdout.write('.')
            stdout.flush()
        try:
            self.record, created = self.model.objects.get_or_create(**filters,
                                                                    defaults=values)
            if created:
                op = CREATED
            else:
                if self.config.always_update or self.is_record_changed(self.record, values):
                    op = UPDATED
                    self.record, __ = self.model.objects.update_or_create(**filters,
                                                                          defaults=values)
                else:
                    op = UNCHANGED
            return op
        except Exception as e:  # pragma: no cover
            raise LoaderException(f"Error in {self}: {e}") from e

    def get_mart_values(self, record=None):
        ret = {'seen': self.context['today']
               }
        if record:
            ret['source_id'] = record.id
        return ret

    def get_final_mapping(self):
        self.mapping = {}
        mart_fields = self.model._meta.concrete_fields
        for field in mart_fields:
            if field.name not in ['country_name', 'schema_name', 'area_code', 'source_id',
                                  'id', 'last_modify_date']:
                self.mapping[field.name] = field.name
        if self.config.mapping:  # pragma: no branch
            self.mapping.update(self.config.mapping)

    def get_values(self, record):
        ret = self.get_mart_values(record)
        for k, v in self.mapping.items():
            if k in ret or v == 'i':
                continue
            else:
                ret[k] = self.get_value(k, v, record, ret)
        return ret

    def get_value(self, field_name, value_or_func, original_record, current_mapping):
        ret = None
        # if value_or_func is None:
        #     ret  None
        if value_or_func == 'N/A':
            ret = 'N/A'
        elif isinstance(value_or_func, str) and hasattr(self, value_or_func) and callable(getattr(self, value_or_func)):
            getter = getattr(self, value_or_func)
            _value = getter(original_record, current_mapping, field_name=field_name)
            if _value != self.noop:
                ret = _value
        elif value_or_func == '-' or hasattr(self, 'get_%s' % field_name):
            getter = getattr(self, 'get_%s' % field_name)
            _value = getter(record=original_record, values=current_mapping, field_name=field_name)
            if _value != self.noop:
                ret = _value
        elif value_or_func == '__self__':
            try:
                ret = self.model.objects.get(source_id=getattr(original_record, field_name).id)
            except AttributeError:
                ret = None
            except self.model.DoesNotExist:
                self.tree_parents.append((original_record.id, getattr(original_record, field_name).id))
                ret = None
        elif callable(value_or_func):
            ret = value_or_func(self, original_record)
        elif value_or_func == '=' and has_attr(original_record, field_name):
            ret = get_attr(original_record, field_name)
        elif not isinstance(value_or_func, str):
            ret = value_or_func
        elif has_attr(original_record, value_or_func):
            ret = get_attr(original_record, value_or_func, undefined)
            if ret == undefined:
                # FIXME: pdb
                import pdb;pdb.set_trace()
                raise ValueError('Invalid mapping. Field:%s Value:%s' % (field_name, value_or_func))
        else:
            raise ValueError(field_name)
        # TODO: remove me
        print(111, "loader.py:350", 11111, field_name, value_or_func, ret)
        return ret

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
                                             table_name=self.config.model._meta.db_table,
                                             defaults={'status': '--'})[0]

    def on_start(self, run_type):
        logger.info(f"Start loader {self}")
        self._start = time.time()
        self.get_final_mapping()
        self.results = EtlResult()

        if self.config.fields_to_compare is None:
            self.fields_to_compare = [f for f in self.mapping.keys() if f not in self.config.exclude_from_compare]
        defs = {'status': 'RUNNING',
                'elapsed': None,
                'results': {},
                'run_type': run_type,
                'last_run': timezone.now()}
        self.etl_task.update(**defs)

    def on_end(self, error=None, retry=False):
        from etools_datamart.apps.subscriptions.models import Subscription
        from django.utils import timezone
        self.results.total_records = self.model.objects.count()

        cost = time.time() - self._start
        defs = {'elapsed': cost,
                'results': self.results.as_dict()}

        if retry:
            defs['status'] = 'RETRY'
            defs['results'] = str(error)
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
                defs['results']['checks'] = self.consistency_check()
        self.etl_task.update(**defs)
        self.etl_task.snapshot()

    def lock(self):
        lock = locks.lock(self.config.lock_key, timeout=self.config.timeout)
        if lock.acquire(blocking=False):
            return lock

    def increment_counter(self, op):
        self.results.incr(op)
        self.context['records'] += 1
        if self.context['max_records'] and self.context['records'] >= self.context['max_records']:
            raise MaxRecordsException

    def update_context(self, **kwargs):
        self.context.update(kwargs)
        return self.context

    def load(self, *, verbosity=0, stdout=None, ignore_dependencies=False, max_records=None,
             only_delta=True, run_type=RUN_UNKNOWN, **kwargs):
        raise NotImplementedError()

    def consistency_check(self):
        pass
