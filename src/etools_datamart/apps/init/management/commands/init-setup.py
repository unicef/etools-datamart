import os

from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from django.core.management.base import BaseCommand
from strategy_field.utils import fqn

from etools_datamart.apps.etl.tasks import load_pmp_indicator


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='select all options but `demo`')
        parser.add_argument(
            '--interactive',
            action='store_true',
            dest='interactive',
            default=False,
            help='select all production deployment options')

        parser.add_argument(
            '--no-migrate',
            action='store_false',
            dest='migrate',
            default=True,
            help='select all production deployment options')

        parser.add_argument(
            '--tasks',
            action='store_true',
            dest='tasks',
            default=False,
            help='schedule tasks')

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        migrate = options['migrate']
        _all = options['all']
        # interactive = options['interactive']

        if migrate or _all:
            call_command('migrate', verbosity=verbosity - 1)

        ModelUser = get_user_model()
        if settings.DEBUG:
            pwd = '123'
            admin = os.environ.get('USER', 'admin')
        else:
            pwd = ModelUser.objects.make_random_password()
            admin = os.environ.get('USER', 'admin')

        self._admin_user, created = ModelUser.objects.get_or_create(username=admin,
                                                                    defaults={"is_superuser": True,
                                                                              "is_staff": True,
                                                                              "password": make_password(pwd)})
        if created:  # pragma: no cover
            self.stdout.write(f"Created superuser `{admin}` with password `{pwd}`")
        else:
            self.stdout.write(f"Superuser `{admin}` already exists`.")

        if options['tasks'] or _all:
            midnight,__ = CrontabSchedule.objects.get_or_create(minute=0, hour=0)
            PeriodicTask.objects.get_or_create(
                name=fqn(load_pmp_indicator.name),
                task=fqn(load_pmp_indicator.name),
                crontab=midnight)
