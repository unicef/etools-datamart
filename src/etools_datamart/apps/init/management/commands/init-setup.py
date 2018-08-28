import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from strategy_field.utils import fqn


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
            midnight, __ = CrontabSchedule.objects.get_or_create(minute=0, hour=0)
            from etools_datamart.celery import app

            tasks = [cls for (name, cls) in app.tasks.items() if name.startswith('etl_')]
            counters = {True: 0, False: 0}
            for task in tasks:
                __, is_new = PeriodicTask.objects.get_or_create(task=fqn(task),
                                                                defaults={'name': task.name,
                                                                          'crontab': midnight})
            for task in PeriodicTask.objects.all():
                try:
                    import_string(task.task)
                except ImportError as e:
                    task.delete()
                    counters[False] += 1

            self.stdout.write(
                f"{PeriodicTask.objects.count()} tasks found. {counters[True]} new. {counters[False]} deleted")

        from unicef_rest_framework.models import Service
        created, deleted, total = Service.objects.load_services()
        self.stdout.write(f"{total} services found. {created} new. {deleted} deleted")
