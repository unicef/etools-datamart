import keyword
import re
from collections import OrderedDict

from django.core.management.base import BaseCommand, CommandError
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.models.constants import LOOKUP_SEP
from django_regex.utils import RegexList

from etools_datamart import state
from etools_datamart.apps.multitenant.admin import format_stm


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, **options):
        from etools_datamart.apps.etools.models import PartnersIntervention
        from etools_datamart.state import state
        state.schemas = ["indonesia"]

        # qs = PartnersIntervention.objects.frs_qs()
        for e in PartnersIntervention.objects.frs_qs():
            # FIXME: remove me (print)
            print(111, e)
