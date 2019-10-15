import inspect

from django.db.models import ForeignKey
from django.utils import timezone

from celery.utils.log import get_task_logger
from constance import config
from strategy_field.utils import get_attr
from temba_client.serialization import TembaObject
from temba_client.v2 import TembaClient
from temba_client.v2.types import ObjectRef

from etools_datamart.apps.etl.loader import (BaseLoader, BaseLoaderOptions, EtlResult,
                                             has_attr, MaxRecordsException, RUN_UNKNOWN,)

logger = get_task_logger(__name__)


class TembaLoaderOptions(BaseLoaderOptions):
    __attrs__ = BaseLoaderOptions.__attrs__ + ['host', 'temba_object']
    DEFAULT_KEY = lambda loader, record: dict(uuid=record.uuid,
                                              organization=loader.context['organization'])


class TembaLoader(BaseLoader):

    def get_fetch_method(self, org):
        return

    def load_organization(self):
        pass

    def get_foreign_key(self, model, ref: ObjectRef):
        if ref:
            return model.objects.get(source_id=ref.uuid)

    def get_mart_values(self, record: TembaObject = None):
        organization = self.context['organization']
        ret = {'organization': organization}
        if record:
            ret['source_id'] = record.uuid
        return ret

    def get_values(self, record: TembaObject):
        # organization = self.context['organization']
        ret = self.get_mart_values(record)
        for dm_field_name, resolver in self.mapping.items():
            remote_attr = getattr(record, resolver, None)
            dm_field = self.model._meta.get_field(resolver)

            if dm_field_name in ret:
                continue

            if resolver is None:
                ret[dm_field_name] = None
            elif resolver == 'N/A':
                ret[dm_field_name] = 'N/A'
            elif resolver == 'i':
                continue
            elif resolver == '-' or hasattr(self, 'get_%s' % dm_field_name):
                getter = getattr(self, 'get_%s' % dm_field_name)
                _value = getter(record, ret, field_name=dm_field_name)
                if _value != self.noop:
                    ret[dm_field_name] = _value
            elif callable(resolver):
                ret[dm_field_name] = resolver(self, record)
            elif resolver == '=' and has_attr(record, dm_field_name):
                ret[dm_field_name] = get_attr(record, dm_field_name)
            elif not isinstance(resolver, str):
                ret[dm_field_name] = resolver
            elif isinstance(resolver, str) and hasattr(self, resolver) and callable(getattr(self, resolver)):
                getter = getattr(self, resolver)
                _value = getter(record, ret, field_name=dm_field_name)
                if _value != self.noop:
                    ret[dm_field_name] = _value
            elif dm_field_name == resolver and isinstance(remote_attr, TembaObject) and isinstance(dm_field,
                                                                                                   ForeignKey):
                ref = getattr(record, resolver, None)
                fk = self.model._meta.get_field(dm_field_name)
                if has_attr(ref, 'uuid'):
                    ret[dm_field_name] = self.get_foreign_key(fk.remote_field.model,
                                                              ref)
            elif has_attr(record, resolver):
                ret[dm_field_name] = get_attr(record, resolver)
            else:
                raise Exception("Invalid field name or mapping '%s:%s'" % (dm_field_name, resolver))

        return ret

    def on_start(self, run_type):
        super().on_start(run_type)

    def on_end(self, error=None, retry=False):
        super().on_end(error, retry)

    def load(self, *, verbosity=0, stdout=None, ignore_dependencies=False, max_records=None,
             only_delta=True, run_type=RUN_UNKNOWN, api_token=None, **kwargs):
        from .models import Source, Organization
        sources = Source.objects.filter(is_active=True)
        self.results = EtlResult()
        try:
            if api_token:
                Source.objects.get_or_create(api_token=api_token,
                                             defaults={'name': api_token})
                sources = sources.filter(api_token=api_token)

            self.on_start(run_type)
            for source in sources:
                if verbosity > 0:
                    stdout.write("Source %s" % source)
                client = TembaClient(config.RAPIDPRO_ADDRESS, source.api_token)
                oo = client.get_org()
                if verbosity > 0:
                    stdout.write("  fetching organization info")

                org, __ = Organization.objects.get_or_create(source=source,
                                                             defaults={'name': oo.name,
                                                                       'country': oo.country,
                                                                       'primary_language': oo.primary_language,
                                                                       'timezone': oo.timezone,
                                                                       'date_style': oo.date_style,
                                                                       'languages': oo.languages,
                                                                       'anon': oo.anon
                                                                       })
                if verbosity > 0:
                    stdout.write("  found organization %s" % oo.name)

                func = "get_%s" % self.config.source
                getter = getattr(client, func)

                args_spec = inspect.getfullargspec(getter)
                if 'after' in args_spec.args and self.etl_task.last_success:
                    filters = dict(after=self.etl_task.last_success)
                else:
                    filters = {}

                data = getter(**filters)
                self.update_context(today=timezone.now(),
                                    max_records=max_records,
                                    verbosity=verbosity,
                                    records=0,
                                    only_delta=only_delta,
                                    is_empty=not self.model.objects.exists(),
                                    stdout=stdout,
                                    organization=source.organization
                                    )
                if verbosity > 0:
                    stdout.write("  fetching data")
                for page in data.iterfetches():
                    for entry in page:
                        self.source_record = entry
                        filters = self.config.key(self, entry)
                        values = self.get_values(entry)

                        # values['organization'] = source.organization
                        # filters = {'uuid': values['uuid']}
                        op = self.process_record(filters, values)
                        self.increment_counter(op)

        except MaxRecordsException:
            pass
        except Exception as e:
            self.on_end(error=e)
            raise
        finally:
            self.on_end()
        return self.results
