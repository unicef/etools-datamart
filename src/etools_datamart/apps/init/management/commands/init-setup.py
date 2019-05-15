import os
import uuid
import warnings
from urllib.parse import urlparse

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.cache import caches
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections
from django.urls import NoReverseMatch

from constance import config
from django_celery_beat.models import CrontabSchedule, IntervalSchedule
from post_office.models import EmailTemplate
from redisboard.models import RedisServer
from strategy_field.utils import fqn

from unicef_rest_framework.models import PeriodicTask
from unicef_rest_framework.models.acl import GroupAccessControl
from unicef_rest_framework.tasks import preload

from etools_datamart.apps.data.loader import loadeables
from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.apps.security.models import SchemaAccessControl

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

RESTRICTED_AREAS = {'234R': ['mpawlowski@unicef.org',
                             'jmege@unicef.org',
                             'nukhan@unicef.org']}


def get_everybody_available_areas():
    conn = connections['etools']
    return [c.schema_name for c in conn.get_tenants()
            if c.business_area_code not in RESTRICTED_AREAS.keys()]


def get_restricted_areas():
    conn = connections['etools']
    return [c.schema_name for c in conn.get_tenants()
            if c.business_area_code in RESTRICTED_AREAS.keys()]


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument(
            '--deploy',
            action='store_true',
            dest='deploy',
            default=False,
            help='run deployment related actions')
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
            '--collectstatic',
            action='store_true',
            dest='collectstatic',
            default=False,
            help='')

        parser.add_argument(
            '--users',
            action='store_true',
            dest='users',
            default=False,
            help='')

        parser.add_argument(
            '--migrate',
            action='store_true',
            dest='migrate',
            default=False,
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

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        migrate = options['migrate']
        _all = options['all']
        deploy = options['deploy']
        if deploy:
            _all = True
        ModelUser = get_user_model()
        locks = caches['lock']
        lock = locks.lock('init-setup', timeout=60 * 10)
        if not lock.acquire(blocking=False):
            self.stderr.write("Another process is running setup. Nothing to do.")
            return ""
        try:
            if options['collectstatic'] or _all:
                self.stdout.write(f"Run collectstatic")
                call_command('collectstatic', verbosity=verbosity - 1, interactive=False)

            if migrate or _all:
                self.stdout.write(f"Run migrations")
                call_command('migrate', verbosity=verbosity - 1)

            self.stdout.write(f"Create group `Public areas access`")
            public_areas, __ = Group.objects.get_or_create(name='Public areas access')
            config.DEFAULT_GROUP = 'Public areas access'

            self.stdout.write(f"Create group `Restricted areas access`")
            restricted_areas, __ = Group.objects.get_or_create(name='Restricted areas access')

            if options['users'] or _all:
                if settings.DEBUG:
                    pwd = '123'
                    admin = os.environ.get('USER', 'admin')
                else:
                    pwd = os.environ.get('ADMIN_PASSWORD', ModelUser.objects.make_random_password())
                    admin = os.environ.get('ADMIN_USERNAME', 'admin')

                self._admin_user, created = ModelUser.objects.get_or_create(username=admin,
                                                                            defaults={"is_superuser": True,
                                                                                      "is_staff": True,
                                                                                      "password": make_password(pwd)})

                if created:  # pragma: no cover
                    self.stdout.write(f"Created superuser `{admin}` with password `{pwd}`")
                else:  # pragma: no cover
                    self.stdout.write(f"Superuser `{admin}` already exists`.")

                self.stdout.write(f"Create anonymous")
                anonymous, created = ModelUser.objects.get_or_create(username='anonymous',
                                                                     defaults={"is_superuser": False,
                                                                               "is_staff": False,
                                                                               "password": make_password(uuid.uuid4())})

                if os.environ.get('AUTOCREATE_USERS'):
                    self.stdout.write("Found 'AUTOCREATE_USERS' environment variable")
                    self.stdout.write("Going to create new users")
                    try:
                        for entry in os.environ.get('AUTOCREATE_USERS').split('|'):
                            email, pwd = entry.split(',')
                            u, created = ModelUser.objects.get_or_create(username=email,
                                                                         defaults={"is_superuser": False,
                                                                                   "is_staff": False,
                                                                                   "password": make_password(pwd)})

                            if created:
                                self.stdout.write(f"Created user {u}")
                                u.groups.add(public_areas)
                            else:  # pragma: no cover
                                self.stdout.write(f"User {u} already exists.")

                    except Exception as e:  # pragma: no cover
                        warnings.warn(f"Unable to create default users. {e}")

            self.stdout.write(f"Grants all schemas to group `Endpoints all access`")
            SchemaAccessControl.objects.update_or_create(group=public_areas,
                                                         defaults={'schemas': get_everybody_available_areas()})

            self.stdout.write(f"Grants all schemas to group `Endpoints all access`")
            SchemaAccessControl.objects.update_or_create(group=restricted_areas,
                                                         defaults={'schemas': get_restricted_areas()})

            from unicef_rest_framework.models import Service
            created, deleted, total = Service.objects.load_services()
            self.stdout.write(f"{total} services found. {created} new. {deleted} deleted")

            for service in Service.objects.all():
                GroupAccessControl.objects.get_or_create(
                    group=public_areas,
                    service=service,
                    serializers=['*'],
                    policy=GroupAccessControl.POLICY_ALLOW
                )
            for area, users in RESTRICTED_AREAS.items():
                for email in users:
                    u, __ = ModelUser.objects.get_or_create(username=email,
                                                            email=email)
                    u.groups.add(public_areas)
                    u.groups.add(restricted_areas)

            # hostname
            for entry, values in settings.CACHES.items():
                loc = values.get('LOCATION', '')
                spec = urlparse(loc)
                if spec.scheme == 'redis':
                    RedisServer.objects.get_or_create(hostname=spec.hostname,
                                                      port=int(spec.port))

            if options['tasks'] or _all or options['refresh']:
                preload_cron, __ = CrontabSchedule.objects.get_or_create(minute=0, hour=1)
                midnight, __ = CrontabSchedule.objects.get_or_create(minute=0, hour=0)
                CrontabSchedule.objects.get_or_create(hour='0, 6, 12, 18')
                CrontabSchedule.objects.get_or_create(hour='0, 12')
                IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.HOURS)

                every_minute, __ = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.MINUTES)

                # tasks = app.get_all_etls()
                counters = {True: 0, False: 0}
                loaders = []
                for loadeable in loadeables:
                    model = apps.get_model(loadeable)
                    loaders.append(model.loader.task.name)
                    __, is_new = PeriodicTask.objects.get_or_create(name=f"ETL {model.loader.task.name}",
                                                                    defaults={'task': model.loader.task.name,
                                                                              'service': Service.objects.get_for_model(
                                                                                  model),
                                                                              'crontab': midnight})
                    if is_new:
                        self.stdout.write(f"NEW load task {model.loader.task.name} scheduled at {midnight}")

                # preload
                for service in Service.objects.all():
                    try:
                        url = service.endpoint
                    except NoReverseMatch:
                        PeriodicTask.objects.filter(service=service).delete()
                        service.delete()
                    else:
                        pp, is_new = PeriodicTask.objects.get_or_create(name=f'PRELOAD {url}',
                                                                        defaults={'task': fqn(preload),
                                                                                  'crontab': preload_cron,
                                                                                  'service': service,
                                                                                  'args': f'["{url}?page_size=-1"]'})
                        if is_new:
                            self.stdout.write(f"NEW preload task for '{url}'")

                ret = PeriodicTask.objects.filter(task__startswith='load_').exclude(task__in=loaders).delete()
                counters[False] = ret[0]

                EtlTask.objects.inspect()
                self.stdout.write(
                    f"{PeriodicTask.objects.filter(name__startswith='data.').count()} "
                    f"periodic task found. {counters[True]} new. {counters[False]} deleted")

                PeriodicTask.objects.get_or_create(task='send_queued_mail',
                                                   defaults={'name': 'process mail queue',
                                                             'interval': every_minute})

                # PeriodicTask.objects.get_or_create(task='send_queued_mail',
                #                                    defaults={'name': 'process mail queue',
                #                                              'interval': every_minute})

            EmailTemplate.objects.get_or_create(name='dataset_changed_attachment',
                                                defaults=dict(subject='Dataset changed',
                                                              content=MAIL_ATTACHMENT,
                                                              html_content=MAIL_ATTACHMENT_HTML))

            EmailTemplate.objects.get_or_create(name='dataset_changed',
                                                defaults=dict(subject='Dataset changed',
                                                              content=MAIL,
                                                              html_content=MAIL_HTML))

            if options['refresh'] or deploy:
                self.stdout.write("Refreshing datamart...")
                for model_name in loadeables:
                    model = apps.get_model(model_name)
                    model.loader.task.delay()

            if deploy:
                Service.objects.invalidate_cache()
                config.CACHE_VERSION = config.CACHE_VERSION + 1
        finally:
            lock.release()
