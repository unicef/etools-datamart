# -*- coding: utf-8 -*-
import logging
import sys

from django.apps import apps
from django.core.management import BaseCommand

from etools_datamart.apps.data.loader import loadeable

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = ''
    requires_system_checks = False
    requires_migrations_checks = False
    output_transaction = False  # Whether to wrap the output in a "BEGIN; COMMIT;"

    def add_arguments(self, parser):
        parser.add_argument('args',
                            metavar='models', nargs='*', help='One or more application label.')
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

    def notify(self, model, created, name, tpl="  {op} {model} `{name}`"):
        if self.verbosity > 2:
            op = {True: "Created", False: "Updated"}[created]
            self.stdout.write(tpl.format(op=op, model=model, name=name))
        elif self.verbosity > 1:
            self.stdout.write('.', ending='')

    def handle(self, *model_names, **options):
        self.verbosity = options['verbosity']
        _all = options['all']
        unlock = options['unlock']
        if _all:
            model_names = sorted(list(loadeable))

        if not model_names:
            for model_name in sorted(list(loadeable)):
                self.stdout.write(model_name)
        else:
            for model_name in model_names:
                model = apps.get_model(model_name)
                if unlock:
                    model.loader.load.unlock()
                res = model.loader.load(always_update=options['ignore_changes'],
                                        stdout=sys.stdout)
                self.stdout.write(f"{model_name:20}: "
                                  f"  created: {res.created:<3}"
                                  f"  updated: {res.updated:<3}"
                                  f"  unchanged: {res.unchanged:<3}\n"
                                  )
