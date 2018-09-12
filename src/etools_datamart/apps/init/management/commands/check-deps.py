# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from etools_datamart.apps.init.checks import check_imports


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
        try:
            check_imports()
        except Exception as e:
            raise CommandError(e)
