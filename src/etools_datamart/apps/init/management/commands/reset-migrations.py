import logging
import os
from glob import iglob
from subprocess import check_call

from django.core.management import BaseCommand, call_command

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = 'Init Setup'
    requires_migrations_checks = False
    requires_system_checks = False

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--noinput', action='store_false',
            dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.')

    def handle(self, *args, **options):
        if options.get('interactive'):
            confirm = input("""
        You have requested to fully reset your migrations.
        This will IRREVERSIBLY DESTROY ALL EXISTING MIGRATIONS.
        This command is intended to reduce the number of migrations created
        during the initial phases of the development and should be performed
        only BEFORE YOUR FIRST DEPLOYMENT IN PRODUCTION
        Are you sure you want to do this?

        Type 'yes' to continue, or 'no' to cancel: """)
        else:
            confirm = 'yes'

        if confirm != 'yes':
            print("Migrations reset cancelled.")
            return

        for filename in iglob('src/**/migrations/0*.py', recursive=True):
            os.unlink(filename)
        call_command('makemigrations')

        check_call("git add src/**/migrations/0*.py", shell=True)
