import keyword
import re
from collections import OrderedDict

from django.core.management.base import BaseCommand, CommandError
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.models.constants import LOOKUP_SEP
from django_regex.utils import RegexList

from etools_datamart import state
from etools_datamart.apps.multitenant.postgresql.utils import clear_schemas


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, **options):
        from etools_datamart.apps.etl.tasks import load_pmp_indicator
        with clear_schemas():
            load_pmp_indicator()
