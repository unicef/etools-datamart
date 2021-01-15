import logging
import time

from django.apps import apps
from django.core.management import BaseCommand
from django.db import connections

# from etools_datamart.apps.data.loader import loadeables, RUN_COMMAND
from etools_datamart.apps.etl.loader import loadeables, RUN_COMMAND
from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.libs.time import strfelapsed

logger = logging.getLogger(__name__)


def setup_logging(verbosity):
    level = {3: logging.DEBUG,
             2: logging.INFO,
             1: logging.ERROR,
             0: logging.NOTSET}[verbosity]

    targets = ['etools_datamart.apps.mart.data.loader']
    consoleLogger = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    consoleLogger.setLevel(logging.DEBUG)
    consoleLogger.setFormatter(formatter)
    rootLogger = logging.getLogger()
    rootLogger.addHandler(consoleLogger)

    for target in targets:
        logger = logging.getLogger(target)
        logger.setLevel(level)
        logger.propagate = False
        logger.addHandler(consoleLogger)


class Command(BaseCommand):
    args = ''
    help = ''
    requires_system_checks = False
    requires_migrations_checks = False
    output_transaction = False  # Whether to wrap the output in a "BEGIN; COMMIT;"

    def add_arguments(self, parser):
        parser.add_argument('args',
                            metavar='models', nargs='*', help='One or more application label.')

        parser.add_argument('-e', '--exclude',
                            metavar='excludes',
                            nargs='*', help='exclude.')

        parser.add_argument(
            '--truncate', action='store_true',
            help="Truncate table before load",
        )

        parser.add_argument(
            '--all', action='store_true',
            help="Run all loaders.",
        )
        parser.add_argument(
            '--api-token', action='store',
            help="RapidPRO token",
        )
        parser.add_argument(
            '--ignore-changes', action='store_true',
            help=".",
        )
        parser.add_argument(
            '--unlock', action='store_true',
            help="Unlock all loaders.",
        )
        parser.add_argument(
            '--no-deps', action='store_true',
            help="Ignore status of required datasets",
        )
        parser.add_argument(
            '--process-deps', action='store_true',
            help="process all dependencies first",
        )

        parser.add_argument(
            '--no-delta', action='store_true',
            help="Do not use last_modify_field if present. Reload full dataset.",
        )

        parser.add_argument(
            '--debug', action='store_true',
            help="maximum logging level",
        )

        parser.add_argument(
            '--elapsed', action='store_true',
            help="measure elapsed time",
        )

        parser.add_argument(
            '--failed', action='store_true',
            help="Run only failed tasks",
        )

        parser.add_argument(
            '--async', action='store_true',
            help="Run only failed tasks",
        )

        parser.add_argument('-c',
                            '--countries',
                            help="Run only selected counries",
                            )

        parser.add_argument('-r',
                            '--records',
                            type=int,
                            help="Only load <n> records",
                            )

    def notify(self, model, created, name, tpl="  {op} {model} `{name}`"):
        if self.verbosity > 2:
            op = {True: "Created", False: "Updated"}[created]
            self.stdout.write(tpl.format(op=op, model=model, name=name))
        elif self.verbosity > 1:
            self.stdout.write('.', ending='')

    def calculate_deps(self, names):
        def process(model):
            queue = []
            for dep in model.loader.config.depends:
                queue.extend(process(dep))
            queue.append("%s.%s" % (model._meta.app_label, model._meta.model_name))
            return queue

        model_names = []
        for m in names:
            model = apps.get_model(m)
            model_names.extend(process(model))
        return model_names

    def handle(self, *model_names, **options):
        self.verbosity = options['verbosity']

        _all = options['all']
        debug = options['debug']
        unlock = options['unlock']
        excludes = options['exclude'] or []
        records = options['records']
        countries = options['countries']
        no_delta = options['no_delta']
        truncate = options['truncate']
        asyncronous = options['async']

        if debug:
            setup_logging(self.verbosity)
        if _all:
            model_names = sorted([m for m in loadeables if m not in excludes])
        elif options['failed']:
            qs = EtlTask.objects.exclude(status__in=['SUCCESS', 'RUNNING'])
            model_names = [t.loader.model_name for t in qs]

        if countries:
            connection = connections['etools']
            schemas = [c for c in connection.get_tenants() if c.schema_name in countries.split(',')]
            # schemas = [c for c in connection.get_tenants() if c.schema_name in ['bangladesh', 'uganda']]
        else:
            schemas = None
        if not model_names:
            for model_name in sorted(list(loadeables)):
                self.stdout.write(model_name)
        else:
            if options['elapsed']:
                global_start_time = time.time()
            if options['process_deps']:
                model_names = self.calculate_deps(model_names)

            try:
                for model_name in model_names:
                    if self.verbosity > 0:
                        self.stdout.write(f"Loading {model_name}")
                    try:
                        model = apps.get_model(model_name)
                    except LookupError:
                        self.stderr.write(f'Invalid model {model_name}')
                        self.stderr.write(f'Available choices are:')
                        for model_name in sorted(list(loadeables)):
                            self.stderr.write(f"  - {model_name}")
                        return ""

                    if unlock:
                        if self.verbosity > 1:
                            self.stdout.write(f"Unlock {model_name}")
                        model.loader.unlock()
                    if truncate:
                        if self.verbosity > 0:
                            self.stdout.write(f"Truncating {model_name}")
                            model.objects.truncate()
                    elapsed = ""
                    if options['elapsed']:
                        start_time = time.time()

                    model.loader.config.always_update = options['ignore_changes']
                    config = dict(api_token=options.get('api_token'),
                                  ignore_dependencies=options['no_deps'],
                                  verbosity=self.verbosity - 1,
                                  run_type=RUN_COMMAND,
                                  max_records=records,
                                  countries=schemas,
                                  only_delta=not no_delta)
                    if asyncronous:
                        aresult = model.loader.task.apply_async(**config)
                        res = aresult.get()
                    else:
                        res = model.loader.load(**config, stdout=self.stdout)
                    if options['elapsed']:
                        elapsed_time = time.time() - start_time
                        elapsed = "in %s" % strfelapsed(elapsed_time)

                    self.stdout.write(f"{model_name:30}: "
                                      f"  created: {res.created:>6}"
                                      f"  updated: {res.updated:>6}"
                                      f"  unchanged: {res.unchanged:>6}"
                                      f"  deleted: {res.deleted:>6}"
                                      f" {elapsed}\n"
                                      )
                if options['elapsed']:
                    global_elapsed_time = time.time() - global_start_time
                    global_elapsed = "in %s" % strfelapsed(global_elapsed_time)
                    self.stdout.write(f"Loadig total time: {global_elapsed}")

            except KeyboardInterrupt:
                return "Interrupted"
