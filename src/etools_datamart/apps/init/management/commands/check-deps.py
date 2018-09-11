# -*- coding: utf-8 -*-
import importlib
import pkgutil

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = ''
    help = 'Imports all modules to check for missed dependencies.'
    requires_migrations_checks = False
    requires_system_checks = False

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def _get_cursor(self, conn):
        conn.cursor()
        return conn

    def handle(self, *args, **options):
        import etools_datamart as package
        ""
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            current_module = '{}.{}'.format(package.__name__, modname)
            m = importlib.import_module(current_module)
            if hasattr(m, '__path__'):
                for _, sub_mod, __ in pkgutil.iter_modules(m.__path__):
                    sub_module = '{}.{}'.format(current_module, sub_mod)
                    sm = importlib.import_module(sub_module)
                    if hasattr(sm, '__path__'):
                        for _, s_sub_mod, __ in pkgutil.iter_modules(sm.__path__):
                            s_sub_mod = '{}.{}.{}'.format(current_module, sub_mod, s_sub_mod)
                            try:
                                importlib.import_module(s_sub_mod)
                            except Exception as e:
                                raise CommandError(f"""Error importing '{s_sub_mod}'.
{e}
""")
