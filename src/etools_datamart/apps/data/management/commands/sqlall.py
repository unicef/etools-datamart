# -*- coding: utf-8 -*-
import logging
import subprocess

from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand, CommandError

import sqlparse
from django_regex.utils import RegexList
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import SqlLexer

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
                            metavar='connections',
                            nargs='*', help='One or more connection label.')

        parser.add_argument(
            '--format', action='store_true',
            help="reformat SQL code ",
        )

        parser.add_argument(
            '--keyword-case', action='store',
            default='upper',
            help="case of SQL keywords",
        )

        parser.add_argument(
            '--models', '-m',
            action='store',
            nargs='*',
            help="filter applications",
        )
        parser.add_argument(
            '--table', '-t',
            dest='tables',
            action='store',
            nargs='*',
            help="filter tables",
        )
        parser.add_argument(
            '--dry-run', '-d',
            action='store_true',
            help="filter tables",
        )
        parser.add_argument(
            '--style', action='store',
            default='default',
            help="case of SQL keywords",
        )

        parser.add_argument(
            '--force-engine',
            action='store_false',
            dest='check_engine',
            help="do not check Engine compatibility",
        )
        parser.add_argument(
            '--no-highlight',
            '-nh',
            dest='highlight',
            action='store_false',
            default=True,
            help="colorize output",
        )

    def handle(self, *connections, **options):
        self.verbosity = options['verbosity']
        if not connections:
            self.stdout.write("\n".join(settings.DATABASES.keys()))
            return
        for conn_name in connections:
            engine = settings.DATABASES[conn_name]['ENGINE']
            if options['check_engine'] and engine not in ['django.contrib.gis.db.backends.postgis',
                                                          'django.contrib.gis.db.backends.postgresql',
                                                          'etools_datamart.apps.multitenant.postgresql']:
                raise CommandError("Engine not supported: '%s'" % engine)

            dbname = settings.DATABASES[conn_name]['NAME']
            uname = settings.DATABASES[conn_name]['USER']
            passw = settings.DATABASES[conn_name]['PASSWORD']
            host = settings.DATABASES[conn_name]['HOST']
            port = settings.DATABASES[conn_name]['PORT']
            cmds = ['pg_dump',
                    dbname,
                    '--schema', 'public',
                    '--schema-only',
                    '--no-owner',
                    '--no-security-labels',
                    '--no-synchronized-snapshots',
                    '--no-tablespaces',
                    '--no-privileges',
                    '-U', uname,
                    '-p', str(port),
                    '-h', host,
                    ]
            if passw:
                cmds.extend(['-W', passw])

            if options['models']:
                requested = RegexList(options['models'])
                models = apps.get_models()
                names = [m._meta.db_table for m in models]
                selection = [n for n in names if n in requested]
                for tablename in selection:
                    cmds.extend(['-t', tablename])

            if options['tables']:
                for tablename in options['tables']:
                    cmds.extend(['-t', tablename])

            if self.verbosity > 1 or options['dry_run']:
                self.stdout.write(" ".join(cmds))

            if not options['dry_run']:
                p = subprocess.Popen(cmds,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, errors = p.communicate()
                if errors:
                    self.stderr.write(errors.decode())
                else:
                    if options['format']:
                        output = sqlparse.format(output,
                                                 strip_comments=True,
                                                 strip_whitespace=True,
                                                 indent_width=2,
                                                 output_format='sql',
                                                 reindent=True,
                                                 keyword_case='upper')
                        lexer = SqlLexer()
                        formatter = Terminal256Formatter(style=options['style'])
                        if options['highlight']:
                            output = highlight(output, lexer, formatter)
                    else:
                        output = output.decode('utf8')

                    self.stdout.write(output)
