import sys
import time

from django.core.management.base import BaseCommand

import psutil
import requests

import etools_datamart


class Command(BaseCommand):
    args = ''
    help = 'Help text here....'
    requires_migrations_checks = False
    requires_system_checks = False

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--pidfile',
            dest='pidfile',
            default=None,
            help='target process pidfile')
        parser.add_argument(
            '--host',
            dest='host',
            default='http://127.0.0.1:8000',
            help='run deployment related actions')
        parser.add_argument(
            '--timeout',
            dest='timeout',
            default=60 * 5,
            help='check timeout')

    def handle(self, *args, **options):
        sleep = 5
        pidfile = options['pidfile']
        timeout = options['timeout']
        host = options['host']
        try:
            if pidfile:
                with open(pidfile, 'r') as f:
                    pid = f.read()
                p = psutil.Process(int(pid))
                stop_at = time.time() + timeout
                while True:
                    if p.is_running() and p.children():
                        break
                    if time.time() > stop_at:
                        sys.exit(1)
                    time.sleep(sleep)

            if host:
                stop_at = time.time() + timeout
                while True:
                    try:
                        url = '%s/healthcheck/%s/' % (host, etools_datamart.VERSION)
                        res = requests.get(url, timeout=1)
                        assert res.status_code == 200
                        self.stdout.write('Success')
                        sys.exit(0)
                    except Exception:
                        self.stdout.write('.', ending='')
                        self.stdout._out.flush()

                    if time.time() > stop_at:
                        sys.exit(1)
                    time.sleep(sleep)
        except KeyboardInterrupt:
            self.stdout.write('')
            sys.exit(1)
