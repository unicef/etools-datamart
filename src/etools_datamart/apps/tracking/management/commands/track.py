import logging
import os
from urllib.parse import urlencode

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = ''
    requires_migrations_checks = False
    requires_system_checks = []

    def add_arguments(self, parser):

        parser.add_argument(
            '--tid',
            action='store_true',
            dest='all',
            default=os.environ.get('ANALYTICS_CODE'),
            help='select all options but `demo`')
        parser.add_argument(
            '--demo',
            action='store_true',
            dest='demo',
            default=False,
            help='create random demo .local')

    def echo(self, txt, st='SUCCESS'):
        if self.verbosity == 0:
            return
        if self.verbosity == 1:
            text = f"{txt}"
        else:
            text = f"\n{txt}"
        self.stdout.write(getattr(self.style, st)(text))

    def notify(self, model, created, name, tpl="  {op} {model} `{name}`"):
        if self.verbosity > 2:
            op = {True: "Created", False: "Updated"}[created]
            self.stdout.write(tpl.format(op=op, model=model, name=name))
        elif self.verbosity > 1:
            self.stdout.write('.', ending='')

    def handle(self, *args, **options):
        self.verbosity = options['verbosity']
        tid = options['tid']
        import requests

        # """https://www.google-analytics.com/r/collect?v=1&_v=j72&a=1254325655&t=pageview&_s=1&dl=http%3A%2F%2Flocalhost%2F&ul=en-gb&de=UTF-8&dt=Title&sd=24-bit&sr=1440x900&vp=1425x459&je=0&_u=IEBAAUAB~&jid=243210006&gjid=1351824934&cid=778822076.1544038618&tid=UA-130479575-1&_gid=909229133.1544038618&_r=1&gtm=2oubc0&z=118711575"""
        values = {
            "v": 1,
            "t": "pageview",
            # "t": "event",
            # "ec": "video",  # event category
            # "ea": "play",  # event action
            # "el": "holiday",
            "tid": tid,
            "cid": 555,
            "ev": 300,
            "dl": "http://datamart.unicef.io/aaaa",

        }
        qs = urlencode(values)
        # payload = 'v=1&t=event&tid=UA-130479575-1&cid=555&ec=video&ea=play&el=holiday&ev=300&dl=http%3A%2F%2Flocalhost%2Fbbb'
        requests.post('http://www.google-analytics.com/collect', data=qs)
