# -*- coding: utf-8 -*-
import logging
import sys

from django.apps import apps
from django.core.management import BaseCommand
from django.db import connections

from etools_datamart.apps.data.loader import loadeables, RUN_COMMAND
from etools_datamart.apps.etl.models import EtlTask

logger = logging.getLogger(__name__)


def setup_logging(verbosity):
    level = {3: logging.DEBUG,
             2: logging.INFO,
             1: logging.ERROR,
             0: logging.NOTSET}[verbosity]

    targets = ['etools_datamart.apps.data.loader']
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
            '--all', action='store_true',
            help="Run all loaders.",
        )
        parser.add_argument(
            '--ignore-changes', action='store_true',
            help="Run all loaders.",
        )
        parser.add_argument(
            '--unlock', action='store_true',
            help="Unlock all loaders.",
        )
        parser.add_argument(
            '--no-deps', action='store_true',
            help="Ingnore status of required datasets",
        )

        parser.add_argument(
            '--ignore-last-modify-field', action='store_true',
            help="Do not use last_modify_field if present. Reload full dataset.",
        )

        parser.add_argument(
            '--debug', action='store_true',
            help="maximum logging level",
        )

        parser.add_argument(
            '--failed', action='store_true',
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

    def handle(self, *model_names, **options):
        self.verbosity = options['verbosity']

        _all = options['all']
        debug = options['debug']
        unlock = options['unlock']
        excludes = options['exclude'] or []
        records = options['records']
        countries = options['countries'].split(',')

        if debug:
            setup_logging(self.verbosity)
        if _all:
            model_names = sorted([m for m in loadeables if m not in excludes])
        elif options['failed']:
            qs = EtlTask.objects.exclude(status__in=['SUCCESS', 'RUNNING'])
            model_names = [t.loader.model_name for t in qs]

        if countries:
            connection = connections['etools']
            schemas = [c for c in connection.get_tenants() if c.schema_name in countries]
        else:
            schemas = None
        if not model_names:
            for model_name in sorted(list(loadeables)):
                self.stdout.write(model_name)
        else:
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
                    res = model.loader.load(always_update=options['ignore_changes'],
                                            ignore_dependencies=options['no_deps'],
                                            verbosity=self.verbosity,
                                            run_type=RUN_COMMAND,
                                            max_records=records,
                                            countries=schemas,
                                            stdout=sys.stdout)
                    self.stdout.write(f"{model_name:20}: "
                                      f"  created: {res.created:<3}"
                                      f"  updated: {res.updated:<3}"
                                      f"  unchanged: {res.unchanged:<3}\n"
                                      )
            except KeyboardInterrupt:
                return "Interrupted"
