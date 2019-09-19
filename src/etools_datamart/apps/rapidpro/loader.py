from django.utils import timezone

from celery.utils.log import get_task_logger
from constance import config
from temba_client.v2 import TembaClient

from etools_datamart.apps.etl.loader import BaseLoader, BaseLoaderOptions, EtlResult, RUN_UNKNOWN

logger = get_task_logger(__name__)

DEFAULT_KEY = lambda loader, record: dict(uuid=record['uuid'],
                                          organization=loader.context['organization'])


class TembaLoaderOptions(BaseLoaderOptions):
    __attrs__ = BaseLoaderOptions.__attrs__ + ['host', 'temba_object']

    def __init__(self, base=None):
        super().__init__(base)
        self.key = DEFAULT_KEY


class TembaLoader(BaseLoader):

    def get_fetch_method(self, org):
        return

    def load_organization(self):
        pass

    def get_mart_values(self, record=None):
        organization = self.context['organization']
        ret = {'organization': organization,
               'seen': self.context['today']
               }
        if record:
            ret['source_id'] = record['uuid']
        return ret

    def get_values(self, record):
        organization = self.context['organization']
        ret = self.get_mart_values(record)

        for k, v in self.mapping.items():
            if k in ret:
                continue
            if v is None:
                ret[k] = None
            elif v == 'N/A':
                ret[k] = 'N/A'
            elif v == 'i':
                continue
            elif isinstance(v, str) and hasattr(self, v) and callable(getattr(self, v)):
                getter = getattr(self, v)
                _value = getter(record, ret, field_name=k)
                if _value != self.noop:
                    ret[k] = _value
            elif v == '-' or hasattr(self, 'get_%s' % k):
                getter = getattr(self, 'get_%s' % k)
                _value = getter(record, ret, field_name=k)
                if _value != self.noop:
                    ret[k] = _value
            elif v == '__self__':
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
                except ObjectDoesNotExist:  # pragma: no cover
                    ret[k] = None
                except AttributeError:  # pragma: no cover
                    pass
            elif callable(v):
                ret[k] = v(self, record)
            elif v == '=' and has_attr(record, k):
                ret[k] = get_attr(record, k)
            # elif has_attr(record, k):
            #     ret[k] = get_attr(record, k)
            elif not isinstance(v, str):
                ret[k] = v
            elif has_attr(record, v):
                ret[k] = get_attr(record, v)
            else:
                raise Exception("Invalid field name or mapping '%s:%s'" % (k, v))

        return ret
    #
    # def get_values(self, record):
    #     return record.serialize()

    def load(self, *, verbosity=0, stdout=None, ignore_dependencies=False, max_records=None,
             only_delta=True, run_type=RUN_UNKNOWN, api_token=None, **kwargs):
        from .models import Source, Organization
        sources = Source.objects.filter(is_active=True)
        self.results = EtlResult()
        try:
            if api_token:
                source, __ = Source.objects.get_or_create(api_token=api_token,
                                                          defaults={'name': api_token})
                client = TembaClient(source.server, api_token)
                sources = sources.filter(api_token=api_token)

            self.on_start(run_type)
            for source in sources:
                client = TembaClient(config.RAPIDPRO_ADDRESS, source.api_token)
                oo = client.get_org()

                org, __ = Organization.objects.get_or_create(source=source,
                                                             defaults={'name': oo.name,
                                                                       'country': oo.country,
                                                                       'primary_language': oo.primary_language,
                                                                       'timezone': oo.timezone,
                                                                       'date_style': oo.date_style,
                                                                       'languages': oo.languages,
                                                                       'anon': oo.anon
                                                                       })

                func = "get_%s" % self.config.source
                getter = getattr(client, func)
                data = getter()
                self.update_context(today=timezone.now(),
                                    max_records=max_records,
                                    verbosity=verbosity,
                                    records=0,
                                    only_delta=only_delta,
                                    is_empty=not self.model.objects.exists(),
                                    stdout=stdout,
                                    organization=source.organization
                                    )

                for entry in data.all():
                    filters = self.config.key(self, entry)
                    values = self.get_values(entry)

                    # values['organization'] = source.organization
                    # filters = {'uuid': values['uuid']}
                    op = self.process_record(filters, values)
                    self.increment_counter(op)

        except Exception as e:
            self.on_end(error=e)
            raise
        finally:
            self.on_end()
        return self.results
