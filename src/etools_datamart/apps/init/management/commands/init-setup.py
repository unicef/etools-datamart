import os
import warnings
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask
from humanize import naturaldelta
from post_office.models import EmailTemplate
from redisboard.models import RedisServer
from strategy_field.utils import fqn
from unicef_rest_framework.models.acl import GroupAccessControl

from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.celery import app

MAIL = r"""Dear {{user.label}},

On {{etl.last_changes|date:"M d, Y"}}, datamart has detected changes in dataset `{{verbose_name}}`.
Please visit {{base_url}}{{service.endpoint}}

—
You are receiving this because you are subscribed to this thread.
To unsubscribe, change your preferences in {{base_url}}{% url 'monitor' %}
"""

MAIL_HTML = r"""<div>Dear {{user.label}},</div>
<div>&nbsp;</div>
<div>On {{etl.last_changes|date:"M d, Y"}}, datamart has detected changes in dataset `{{verbose_name}}`.</div>
<div>You can view data following this <a href="{{base_url}}{{service.endpoint}}">link</a>
 or download the as <a href="{{base_url}}{{service.endpoint}}?format=xlsx">excel</a></div>
<div>&nbsp;</div>
<div>&nbsp;</div>
<div>&nbsp;</div>
<div>-</div>
<div>You are receiving this because you are subscribed to this thread.</div>
<div>To unsubscribe, change your preferences in <a href="{{base_url}}{% url 'monitor' %}">Datamart Monitor</a></div>
"""

MAIL_ATTACHMENT = r"""Dear {{user.label}},

On {{etl.last_changes|date:"M d, Y"}}, datamart has detected changes in dataset `{{verbose_name}}`.
You can find here in attachment a excel file with updated data

—
You are receiving this because you are subscribed to this thread.
To unsubscribe, change your preferences in {{base_url}}{% url 'monitor' %}
"""

MAIL_ATTACHMENT_HTML = r"""<div>Dear {{user.label}},</div>
<div>&nbsp;</div>
<div>On {{etl.last_changes|date:"M d, Y"}}, datamart has detected changes in dataset `{{verbose_name}}`.</div>
<div>Attached to this email you can find excel file with updated data</div>
<div>&nbsp;</div>
<div>&nbsp;</div>
<div>&nbsp;</div>
<div>-</div>
<div>You are receiving this because you are subscribed to this thread.</div>
<div>To unsubscribe, change your preferences in <a href="{{base_url}}{% url 'monitor' %}">Datamart Monitor</a></div>
"""


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

        parser.add_argument(
            '--refresh',
            action='store_true',
            dest='refresh',
            default=False,
            help='refresh datamart tables')

        parser.add_argument(
            '--async',
            action='store_true',
            dest='_async',
            default=False,
            help='use celery to refresh datamart')

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
        Group.objects.get_or_create(name='Guests')
        all_access, __ = Group.objects.get_or_create(name='Endpoints all access')

        if created:  # pragma: no cover
            self.stdout.write(f"Created superuser `{admin}` with password `{pwd}`")
        else:  # pragma: no cover
            self.stdout.write(f"Superuser `{admin}` already exists`.")

        from unicef_rest_framework.models import Service
        created, deleted, total = Service.objects.load_services()
        self.stdout.write(f"{total} services found. {created} new. {deleted} deleted")
        if os.environ.get('INVALIDATE_CACHE'):
            Service.objects.invalidate_cache()

        for service in Service.objects.all():
            GroupAccessControl.objects.get_or_create(
                group=all_access,
                service=service,
                serializers=['*'],
                policy=GroupAccessControl.POLICY_ALLOW
            )
        # hostname
        for entry, values in settings.CACHES.items():
            loc = values.get('LOCATION', '')
            spec = urlparse(loc)
            if spec.scheme == 'redis':
                RedisServer.objects.get_or_create(hostname=spec.netloc,
                                                  port=int(spec.port))

        if os.environ.get('AUTOCREATE_USERS'):
            self.stdout.write("Found 'AUTOCREATE_USERS' environment variable")
            self.stdout.write("Going to create new users")
            try:
                for entry in os.environ.get('AUTOCREATE_USERS').split('|'):
                    user, pwd = entry.split(',')
                    User = get_user_model()
                    u, created = User.objects.get_or_create(username=user)
                    if created:
                        self.stdout.write(f"Created user {u}")
                        u.set_password(pwd)
                        u.save()
                        u.groups.add(all_access)
                    else:  # pragma: no cover
                        self.stdout.write(f"User {u} already exists.")

            except Exception as e:  # pragma: no cover
                warnings.warn(f"Unable to create default users. {e}")

        if options['tasks'] or _all or options['refresh']:
            midnight, __ = CrontabSchedule.objects.get_or_create(minute=0, hour=0)
            CrontabSchedule.objects.get_or_create(hour=[0, 6, 12, 18])
            CrontabSchedule.objects.get_or_create(hour=[0, 12])
            IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.HOURS)

            every_minute, __ = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.MINUTES)

            tasks = app.get_all_etls()
            counters = {True: 0, False: 0}
            for task in tasks:
                __, is_new = PeriodicTask.objects.get_or_create(task=fqn(task),
                                                                defaults={'name': task.name,
                                                                          'crontab': midnight})
            for task in PeriodicTask.objects.all():
                try:
                    import_string(task.task)
                except ImportError:
                    task.delete()
                    counters[False] += 1

            EtlTask.objects.inspect()
            self.stdout.write(
                f"{PeriodicTask.objects.count()} tasks found. {counters[True]} new. {counters[False]} deleted")

            PeriodicTask.objects.get_or_create(task='send_queued_mail',
                                               defaults={'name': 'process mail queue',
                                                         'interval': every_minute})

        EmailTemplate.objects.get_or_create(name='dataset_changed_attachment',
                                            defaults=dict(subject='Dataset changed',
                                                          content=MAIL_ATTACHMENT,
                                                          html_content=MAIL_ATTACHMENT_HTML))

        EmailTemplate.objects.get_or_create(name='dataset_changed',
                                            defaults=dict(subject='Dataset changed',
                                                          content=MAIL,
                                                          html_content=MAIL_HTML))

        if options['refresh']:
            self.stdout.write("Refreshing datamart...")
            for task in PeriodicTask.objects.all()[1:]:
                try:
                    etl = import_string(task.task)
                except ImportError:
                    continue
                self.stdout.write(f"Running {task.name}...", ending='\r')
                self.stdout.flush()

                if options['_async']:
                    etl.delay()
                    self.stdout.write(f"{task.name} scheduled")
                else:
                    etl.apply()
                    cost = naturaldelta(app.timers[task.name])
                    self.stdout.write(f"{task.name} excuted in {cost}")
