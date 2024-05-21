import time
from datetime import timedelta
from inspect import isclass

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import connections, models, transaction
from django.utils import timezone

from celery.utils.log import get_task_logger
from dateutil.utils import today
from dynamic_serializer.core import get_attr
from redis.exceptions import LockError

from etools_datamart.apps.etl.exceptions import MaxRecordsException, RequiredIsMissing, RequiredIsRunning
from etools_datamart.apps.etl.loader import BaseLoader, BaseLoaderOptions, cache, EtlResult, has_attr, RUN_UNKNOWN
from etools_datamart.libs.time import strfelapsed
from etools_datamart.sentry import process_exception

logger = get_task_logger(__name__)


class EToolsLoaderOptions(BaseLoaderOptions):
    DEFAULT_KEY = lambda loader, record: dict(schema_name=loader.context["country"].schema_name, source_id=record.pk)


#     def __init__(self, base=None):
#         super().__init__(base)
#         self.key = lambda loader, record: dict(schema_name=loader.context['country'].schema_name,
#                                                source_id=record.pk)


class EtoolsLoader(BaseLoader):
    def get_mart_values(self, record=None):
        country = self.context["country"]
        ret = {
            "area_code": country.business_area_code,
            "schema_name": country.schema_name,
            "country_name": country.name,
            "seen": self.context["today"],
        }
        if record:
            ret["source_id"] = record.id
        return ret

    def xxget_values(self, record):
        country = self.context["country"]
        ret = self.get_mart_values(record)

        for k, v in self.mapping.items():
            if k in ret:
                continue
            if v is None:
                ret[k] = None
            elif v == "N/A":
                ret[k] = "N/A"
            elif v == "i":
                continue
            elif isinstance(v, str) and hasattr(self, v) and callable(getattr(self, v)):
                getter = getattr(self, v)
                _value = getter(record, ret, field_name=k)
                if _value != self.noop:
                    ret[k] = _value
            elif v == "-" or hasattr(self, "get_%s" % k):
                getter = getattr(self, "get_%s" % k)
                _value = getter(record, ret, field_name=k)
                if _value != self.noop:
                    ret[k] = _value
            elif v == "__self__":
                try:
                    ret[k] = self.model.objects.get(schema_name=country.schema_name, source_id=getattr(record, k).id)
                except AttributeError:
                    ret[k] = None
                except self.model.DoesNotExist:
                    ret[k] = None
                    self.tree_parents.append((record.id, getattr(record, k).id))

            elif isclass(v) and issubclass(v, models.Model):
                try:
                    ret[k] = v.objects.get(schema_name=country.schema_name, source_id=getattr(record, k).id)
                except ObjectDoesNotExist:  # pragma: no cover
                    ret[k] = None
                except AttributeError:  # pragma: no cover
                    pass
            elif callable(v):
                ret[k] = v(self, record)
            elif v == "=" and has_attr(record, k):
                ret[k] = get_attr(record, k)
            # elif has_attr(record, k):
            #     ret[k] = get_attr(record, k)
            elif not isinstance(v, str):
                ret[k] = v
            elif has_attr(record, v):
                ret[k] = get_attr(record, v)
            else:
                raise Exception("Invalid field name or mapping '%s:%s'" % (k, v))

            # enforce field size limit
            # try:
            #     ret[k] = ret[k][:settings.FIELD_SIZE_LIMIT]
            # except TypeError:
            #     not subscriptable so ignoring
            #     pass

        return ret

    def get_value(self, field_name, value_or_func, original_record, current_mapping):
        if value_or_func == "__self__":
            country = self.context["country"]
            try:
                return self.model.objects.get(
                    schema_name=country.schema_name, source_id=getattr(original_record, field_name).id
                )
            except AttributeError:
                return None
            except self.model.DoesNotExist:
                self.tree_parents.append((original_record.id, getattr(original_record, field_name).id))
                return None
        if isclass(value_or_func) and issubclass(value_or_func, models.Model):
            country = self.context["country"]
            try:
                return value_or_func.objects.get(
                    schema_name=country.schema_name, source_id=getattr(original_record, field_name).id
                )
            except ObjectDoesNotExist:  # pragma: no cover
                return None
            except AttributeError:  # pragma: no cover
                pass
        else:
            return super().get_value(field_name, value_or_func, original_record, current_mapping)

    def filter_queryset(self, qs):
        use_delta = self.context["only_delta"] and not self.context["is_empty"]
        if self.config.filters:
            qs = qs.filter(**self.config.filters)
        if use_delta and (self.config.last_modify_field and self.last_run):
            logger.debug(f"Loader {self}: use deltas")
            qs = qs.filter(**{f"{self.config.last_modify_field}__gte": self.last_run})
        return qs

    def process_country(self):
        batch_size = settings.RESULTSET_BATCH_SIZE
        logger.debug(f"Batch size:{batch_size}")

        qs = self.filter_queryset(self.get_queryset())

        paginator = Paginator(qs, batch_size)
        for page_idx in paginator.page_range:
            page = paginator.page(page_idx)
            for record in page.object_list:
                filters = self.config.key(self, record)
                values = self.get_values(record)
                op = self.process_record(filters, values)
                self.increment_counter(op)

    def remove_deleted(self):
        country = self.context["country"]
        existing = list(self.get_queryset().only("id").values_list("id", flat=True))
        to_delete = self.model.objects.filter(schema_name=country.schema_name).exclude(source_id__in=existing)
        if self.config.archive_delta and self.config.archive_field:
            archived_excluded = {f"{self.config.archive_field}__lt": today() - timedelta(self.config.archive_delta)}
            to_delete = to_delete.exclude(**archived_excluded)
        self.results.deleted += to_delete.count()
        to_delete.delete()

    def post_process_country(self):
        country = self.context["country"]
        for mart, etools in self.tree_parents:
            kk = self.model.objects.get(schema_name=country.schema_name, source_id=mart)
            kk.parent = self.model.objects.get(schema_name=country.schema_name, source_id=etools)
            kk.save()
        self.tree_parents = []
        # mark seen records

    def get_queryset(self):
        if self.config.queryset:
            ret = self.config.queryset()
        elif self.config.source:
            ret = self.config.source.objects.all()
        else:  # pragma: no cover
            raise ValueError("Option must define 'queryset' or 'source' attribute")

        return ret

    def load(
        self,
        *,
        verbosity=0,
        stdout=None,
        ignore_dependencies=False,
        max_records=None,
        only_delta=True,
        run_type=RUN_UNKNOWN,
        **kwargs,
    ):
        logger.debug(f"Running loader {self}")
        lock = self.lock()
        truncate = self.config.truncate
        try:
            self.on_start(run_type)
            if lock:  # pragma: no branch
                if not ignore_dependencies:
                    for requirement in self.config.depends:
                        if requirement.loader.is_running():
                            raise RequiredIsRunning(requirement)
                        requirement.loader.check_refresh()
                connection = connections["etools"]
                if kwargs.get("countries"):
                    countries = kwargs["countries"]
                    truncate = False
                else:
                    countries = connection.get_tenants()
                # self.get_final_mapping()
                # if self.config.fields_to_compare is None:
                #     self.fields_to_compare = [f for f in self.mapping.keys() if f not in ["seen"]]

                # self.mapping = {}
                # mart_fields = self.model._meta.concrete_fields
                # for field in mart_fields:
                #     if field.name not in ['country_name', 'schema_name', 'area_code', 'source_id',
                #                           'id', 'last_modify_date']:
                #         self.mapping[field.name] = field.name
                # if self.config.mapping:  # pragma: no branch
                #     self.mapping.update(self.config.mapping)
                self.update_context(
                    today=timezone.now(),
                    countries=countries,
                    max_records=max_records,
                    verbosity=verbosity,
                    records=0,
                    only_delta=only_delta,
                    is_empty=not self.model.objects.exists(),
                    stdout=stdout,
                )
                sid = transaction.savepoint()
                total_countries = len(countries)
                try:
                    self.results.context = self.context
                    # self.fields_to_compare = se
                    # self.fields_to_compare = [f for f in self.mapping.keys() if f not in ["seen"]]
                    if truncate:
                        self.model.objects.truncate()
                    for i, country in enumerate(countries, 1):
                        cache.set("STATUS:%s" % self.etl_task.task, "%s - %s" % (country, self.results.processed))
                        self.context["country"] = country
                        if stdout and verbosity > 0:
                            stdout.write(
                                f"{i:>3}/{total_countries} " f"{country.name:<25} " f"{country.schema_name:<25}"
                            )
                            stdout.flush()

                        connection.set_schemas([country.schema_name])
                        start_time = time.time()

                        self.process_country()
                        elapsed_time = time.time() - start_time
                        elapsed = strfelapsed(elapsed_time)
                        if stdout and verbosity > 0:
                            stdout.write(f"   in {elapsed}\n")
                            stdout.flush()

                        if stdout and verbosity > 2:
                            stdout.write("\n")
                            stdout.flush()
                        self.post_process_country()
                        if self.config.sync_deleted_records(self):
                            self.remove_deleted()
                    if stdout and verbosity > 0:
                        stdout.write("\n")
                except MaxRecordsException:
                    pass
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
            cache.set("STATUS:%s" % self.etl_task.task, "completed - %s" % self.results.processed)
        finally:
            if lock:  # pragma: no branch
                try:
                    lock.release()
                except LockError as e:  # pragma: no cover
                    logger.warning(e)
        return self.results


class CommonSchemaLoaderOptions(BaseLoaderOptions):
    DEFAULT_KEY = lambda loader, record: dict(source_id=record.pk)


class CommonSchemaLoader(EtoolsLoader):
    def get_mart_values(self, record=None):
        ret = {"seen": self.context["today"]}
        if record:
            ret["source_id"] = record.id
        return ret

    def ssget_values(self, record):
        ret = self.get_mart_values(record)

        for k, v in self.mapping.items():
            if v == "__self__":
                try:
                    ret[k] = self.model.objects.get(source_id=getattr(record, k).id)
                except AttributeError:
                    ret[k] = None
                except self.model.DoesNotExist:
                    ret[k] = None
                    self.tree_parents.append((record.id, getattr(record, k).id))

            elif isclass(v) and issubclass(v, models.Model):
                try:
                    ret[k] = v.objects.get(source_id=getattr(record, k).id)
                except AttributeError:  # pragma: no cover
                    pass
            elif callable(v):
                ret[k] = v(self, record)
            elif hasattr(self, "get_%s" % v):
                getter = getattr(self, "get_%s" % v)
                ret[k] = getter(record, ret)
            else:
                ret[k] = get_attr(record, v)

            # enforce field size limit
            # try:
            #     ret[k] = ret[k][:settings.FIELD_SIZE_LIMIT]
            # except TypeError:
            #     # not subscriptable so ignoring
            #     pass

        return ret

    def get_value(self, field_name, value_or_func, original_record, current_mapping):
        if isclass(value_or_func) and issubclass(value_or_func, models.Model):
            try:
                return value_or_func.objects.get(source_id=getattr(original_record, field_name).id)
            except AttributeError:  # pragma: no cover
                pass
        else:
            return super().get_value(field_name, value_or_func, original_record, current_mapping)

    def load(
        self,
        *,
        verbosity=0,
        stdout=None,
        ignore_dependencies=False,
        max_records=None,
        only_delta=True,
        run_type=RUN_UNKNOWN,
        **kwargs,
    ):
        self.on_start(run_type)
        self.results = EtlResult()
        logger.debug(f"Running loader {self}")
        lock = self.lock()
        truncate = self.config.truncate
        try:
            if lock:  # pragma: no branch
                if not ignore_dependencies:
                    for requirement in self.config.depends:
                        if requirement.loader.is_running():
                            raise RequiredIsRunning(requirement)
                        requirement.loader.check_refresh()
                self.mapping = {}
                mart_fields = self.model._meta.concrete_fields
                for field in mart_fields:
                    if field.name not in [
                        "country_name",
                        "schema_name",
                        "area_code",
                        "source_id",
                        "id",
                        "last_modify_date",
                    ]:
                        self.mapping[field.name] = field.name
                if self.config.mapping:  # pragma: no branch
                    self.mapping.update(self.config.mapping)
                self.update_context(
                    today=timezone.now(),
                    max_records=max_records,
                    verbosity=verbosity,
                    records=0,
                    only_delta=only_delta,
                    is_empty=not self.model.objects.exists(),
                    stdout=stdout,
                )
                sid = transaction.savepoint()
                try:
                    self.results.context = self.context
                    self.fields_to_compare = [f for f in self.mapping.keys() if f not in ["seen"]]
                    if truncate:
                        self.model.objects.truncate()
                    self.process_country()
                    if self.config.sync_deleted_records(self):
                        self.remove_deleted()
                    if stdout and verbosity > 0:
                        stdout.write("\n")
                    # deleted = self.model.objects.exclude(seen=today).delete()[0]
                    # self.results.deleted = deleted
                except MaxRecordsException:
                    pass
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
