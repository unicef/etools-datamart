# -*- coding: utf-8 -*-
import logging

from django.core.management import BaseCommand

from unicef_rest_framework.config import conf
from unicef_rest_framework.models import Service

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = ''

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='select all options but `demo`')

    def handle(self, *args, **options):
        router = conf.ROUTER

        list_name = router.routes[0].name
        for prefix, viewset, basename in router.registry:
            service, ok = Service.objects.check_or_create(prefix,
                                                          viewset,
                                                          basename,
                                                          list_name.format(basename=basename)
                                                          )
        for service in Service.objects.order_by('name'):
            print("{0.id:4} {0.name:30} {0.endpoint:40}".format(service))
