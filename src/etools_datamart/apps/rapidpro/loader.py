from django.utils import timezone

from celery.utils.log import get_task_logger
from constance import config
from temba_client.v2 import TembaClient

from etools_datamart.apps.etl.loader import BaseLoader, BaseLoaderOptions, EtlResult, RUN_UNKNOWN

logger = get_task_logger(__name__)


class TembaLoaderOptions(BaseLoaderOptions):
    __attrs__ = BaseLoaderOptions.__attrs__ + ['host', 'temba_object']


class TembaLoader(BaseLoader):

    def get_fetch_method(self, org):
        return

    def load_organization(self):
        pass

    def load(self, *, verbosity=0, stdout=None, ignore_dependencies=False, max_records=None,
             only_delta=True, run_type=RUN_UNKNOWN, api_token=None, **kwargs):
        from .models import Source, Organization
        sources = Source.objects.all()
        self.results = EtlResult()
        try:
            if api_token:
                source, __ = Source.objects.get_or_create(api_token=api_token,
                                                          defaults={'name': api_token})
                client = TembaClient(source.server, api_token)
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
                sources = sources.filter(api_token=api_token)
            self.on_start(run_type)
            for source in sources:
                client = TembaClient(config.RAPIDPRO_ADDRESS, source.api_token)
                func = "get_%s" % self.config.source
                getter = getattr(client, func)
                data = getter()
                self.update_context(today=timezone.now(),
                                    max_records=max_records,
                                    verbosity=verbosity,
                                    records=0,
                                    only_delta=only_delta,
                                    is_empty=not self.model.objects.exists(),
                                    stdout=stdout
                                    )

                for entry in data.all():
                    values = entry.serialize()
                    values['organization'] = source.organization
                    filters = {'uuid': values.get('uuid')}
                    op = self.process_record(filters, values)
                    self.increment_counter(op)

        except Exception as e:
            self.on_end(error=e)
            raise
        finally:
            self.on_end()
        return self.results