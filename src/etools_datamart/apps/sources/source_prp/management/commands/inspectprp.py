# -*- coding: utf-8 -*-
import logging
import re
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

from django.core.management import call_command, CommandError
from django.core.management.commands.inspectdb import Command as BaseCommand
from django.db import connections

from django_regex.utils import RegexList

logger = logging.getLogger(__name__)

INGNORED_TABLES = RegexList([
    'auth_permission',
    'account_user_user_permissions',
    'auth_group_permissions',
    'django_cron_.*',
    'post_office_.*',
    'django_session',
    'drfpasswordless_.*',
    'djcelery_.*',
    'django_migrations',
    'django_admin_log',
    'unicef_notification_.*',
    'celery_.*',
    'social_auth_.*'
])
NO_API = RegexList([
    'AccountUserGroups',
    'AccountUser',
    'AccountUserUserPermissions',
    'AccountUserprofile',
    'Auth.*',
    'Django.*'
])

REVERSE_RELATION_NAMES = {
    # '{model_name}.{att_name}': 'related_name'
}

APPS = ['Unicef', 'Partner', 'Indicator', 'Django', 'Core', 'Cluster', 'Account']


class Command(BaseCommand):
    args = ''
    help = "Introspects PRP database outputs a etools_datamart.apps.prp.models module."
    db_module = 'django.contrib.gis.db'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app_label', default='source_prp', type=str,
            help='application name',
        )

    def handle(self, *args, **options):
        options['database'] = 'prp'
        options['include_partitions'] = False
        options['include_views'] = False
        options['table'] = None
        options['table_name_filter'] = lambda table_name: table_name not in INGNORED_TABLES
        self.prp_models = []

        try:
            output_file = Path(__file__).parent.parent.parent / 'models.py'
            if output_file.exists():
                output_file.rename(output_file.with_suffix('.bak'))
            with output_file.open('w') as output:
                for line in self.handle_inspection(options):
                    output.write("%s\n" % line)
            self.handle_admin(options)
            self.handle_api(options)
            call_command('check')
        except NotImplementedError:
            raise CommandError("Database inspection isn't supported for the currently selected database backend.")

    def handle_model_admin(self, model_name):
        yield ""
        yield "@register(models.%s)" % model_name
        yield "class %sAdmin(DatamartSourceModelAdmin, ModelAdmin):" % model_name
        yield "    list_filter = []"
        yield ""

    def handle_admin(self, options):
        output_file = Path(__file__).parent.parent.parent / 'admin.py'
        if output_file.exists():
            output_file.rename(output_file.with_suffix('.bak'))
        with output_file.open('w') as output:
            output.write("from django.contrib.admin import ModelAdmin, register\n\n")
            output.write("from etools_datamart.apps.core.admin_mixins "
                         "import DatamartSourceModelAdmin\n\n")
            output.write("from . import models\n\n")

            for model_name in self.prp_models:
                for line in self.handle_model_admin(model_name):
                    output.write("%s\n" % line)

    def handle_api(self, options):
        verbosity = options['verbosity']

        api_file = Path(__file__).parent.parent.parent / 'api.py'
        urls_file = Path(__file__).parent.parent.parent / 'api_urls.py'
        if urls_file.exists():
            urls_file.rename(urls_file.with_suffix('.bak'))
        if api_file.exists():
            api_file.rename(api_file.with_suffix('.bak'))
        with urls_file.open('w') as urls:
            urls.write("from etools_datamart.api.urls import router\n\n")
            urls.write("from . import api\n\n")
            with api_file.open('w') as api:
                api.write("from unicef_rest_framework.views import URFReadOnlyModelViewSet\n\n")
                api.write("from etools_datamart.api.endpoints.etools import serializers\n")
                api.write("from etools_datamart.apps.sources.source_prp import models\n")

                for model_name in self.prp_models:
                    if model_name not in NO_API:
                        if verbosity >= 2:
                            self.stdout.write("Generating endpoint for %s" % model_name)
                        for line in self.handle_viewset(model_name):
                            api.write("%s\n" % line)
                        line = "router.register(r'prp/%s', api.%sViewSet)" % (model_name.lower(), model_name)
                        urls.write("%s\n" % line)
                    else:
                        if verbosity >= 1:
                            self.stdout.write("Ignoring endpoint for %s" % model_name)

    def handle_viewset(self, model_name):
        yield ""
        yield ""
        yield "class %sSerializer(serializers.ModelSerializer):" % model_name
        yield "    class Meta:"
        yield "        model = models.%s" % model_name
        yield "        exclude = ()"
        yield ""
        yield ""
        yield "class %sViewSet(URFReadOnlyModelViewSet):" % model_name
        yield "    serializer_class = %sSerializer" % model_name
        yield "    queryset = models.%s.objects.all()" % model_name

    # def handle_urls(self):
    #     output_file = Path(__file__).parent.parent.parent / 'api_urls.py'
    #     if output_file.exists():
    #         output_file.rename(output_file.with_suffix('.bak'))
    #     with output_file.open('w') as output:
    #         output.write("from etools_datamart.api.urls import router\n\n")
    #         output.write("from . import api\n\n")
    #
    #         for model_name in self.prp_models:
    #             line = "router.register(r'prp/%s', api.%sViewSet)" % (model_name.lower(), model_name)
    #             output.write("%s\n" % line)

    def handle_inspection(self, options):
        connection = connections[options['database']]
        # 'table_name_filter' is a stealth option
        table_name_filter = options.get('table_name_filter')
        app_label = options.get('app_label')

        def table2model(table_name):
            return re.sub(r'[^a-zA-Z0-9]', '', table_name.title())

        with connection.cursor() as cursor:
            yield "# flake8: noqa F405."
            yield "# This is an auto-generated PRP model module."
            yield "# Generated on %s" % datetime.now()
            yield 'from %s import models\n' % self.db_module
            yield 'from etools_datamart.apps.core.readonly import ReadOnlyModel'
            known_models = []
            table_info = connection.introspection.get_table_list(cursor)

            # Determine types of tables and/or views to be introspected.
            types = {'t'}
            if options['include_partitions']:
                types.add('p')
            if options['include_views']:
                types.add('v')

            for table_name in (options['table'] or sorted(info.name for info in table_info if info.type in types)):
                if table_name_filter is not None and callable(table_name_filter):
                    if not table_name_filter(table_name):
                        continue
                model_name = table2model(table_name)
                self.prp_models.append(model_name)
                try:
                    try:
                        relations = connection.introspection.get_relations(cursor, table_name)
                    except NotImplementedError:
                        relations = {}
                    try:
                        constraints = connection.introspection.get_constraints(cursor, table_name)
                    except NotImplementedError:
                        constraints = {}
                    primary_key_column = connection.introspection.get_primary_key_column(cursor, table_name)
                    unique_columns = [
                        c['columns'][0] for c in constraints.values()
                        if c['unique'] and len(c['columns']) == 1
                    ]
                    table_description = connection.introspection.get_table_description(cursor, table_name)
                except Exception as e:
                    yield "# Unable to inspect table '%s'" % table_name
                    yield "# The error was: %s" % e
                    continue

                yield ''
                yield ''
                yield 'class %s(ReadOnlyModel):' % table2model(table_name)
                known_models.append(table2model(table_name))
                used_column_names = []  # Holds column names used in the table so far
                column_to_field_name = {}  # Maps column names to names of model fields
                for row in table_description:
                    comment_notes = []  # Holds Field notes, to be displayed in a Python comment.
                    extra_params = OrderedDict()  # Holds Field parameters such as 'db_column'.
                    column_name = row.name
                    is_relation = column_name in relations

                    att_name, params, notes = self.normalize_col_name(
                        column_name, used_column_names, is_relation)
                    extra_params.update(params)
                    comment_notes.extend(notes)

                    used_column_names.append(att_name)
                    column_to_field_name[column_name] = att_name
                    if column_name == 'id':
                        continue
                    # Add primary_key and unique, if necessary.
                    if column_name == primary_key_column:
                        extra_params['primary_key'] = True
                    elif column_name in unique_columns:
                        extra_params['unique'] = True

                    if is_relation:
                        rel_to = (
                            "self" if relations[column_name][1] == table_name
                            else table2model(relations[column_name][1])
                        )
                        # if rel_to in known_models:
                        #     field_type = 'ForeignKey(%s' % rel_to
                        # else:
                        #     field_type = "ForeignKey('%s'" % rel_to
                        if 'unique' in extra_params:
                            extra_params.pop('unique')
                            ftype = 'OneToOneField'
                        elif 'primary_key' in extra_params:
                            extra_params.pop('primary_key')
                            ftype = 'OneToOneField'
                        else:
                            ftype = 'ForeignKey'

                        if rel_to in known_models:
                            field_type = f"{ftype}({rel_to}"
                        else:
                            if rel_to == 'self':
                                field_type = f"{ftype}('self'"
                            else:
                                field_type = f"{ftype}('{app_label}.{rel_to}'"

                    else:
                        # Calling `get_field_type` to get the field type string and any
                        # additional parameters and notes.
                        field_type, field_params, field_notes = self.get_field_type(connection, table_name, row)
                        extra_params.update(field_params)
                        comment_notes.extend(field_notes)

                        field_type += '('

                    # Don't output 'id = meta.AutoField(primary_key=True)', because
                    # that's assumed if it doesn't exist.
                    if att_name == 'id' and extra_params == {'primary_key': True}:
                        if field_type == 'AutoField(':
                            continue
                        elif field_type == 'IntegerField(' and not connection.features.can_introspect_autofield:
                            comment_notes.append('AutoField?')

                    # Add 'null' and 'blank', if the 'null_ok' flag was present in the
                    # table description.
                    if row.null_ok:  # If it's NULL...
                        extra_params['blank'] = True
                        extra_params['null'] = True

                    field_desc = '%s = %s%s' % (
                        att_name,
                        # Custom fields will have a dotted path
                        # '' if '.' in field_type else 'models.',
                        'models.',
                        field_type,
                    )
                    # if field_type.startswith('ForeignKey('):
                    #     field_desc += ', models.DO_NOTHING'
                    if field_type.startswith('ForeignKey(') or field_type.startswith('OneToOneField('):
                        # _related_name = f'{table2model(relations[column_name][1]).lower()}_{table_name}_{column_name}'
                        _related_name = f'{model_name}.{att_name}'

                        if _related_name in REVERSE_RELATION_NAMES:
                            _related_name = REVERSE_RELATION_NAMES[_related_name]
                        else:
                            _related_name = _related_name.replace('.', '_')
                            # _related_name = '+'
                        field_desc += ', models.PROTECT'
                        field_desc += f", related_name='{_related_name}'"

                    if extra_params:
                        if not field_desc.endswith('('):
                            field_desc += ', '
                        field_desc += ', '.join('%s=%r' % (k, v) for k, v in extra_params.items())
                    field_desc += ')'
                    if comment_notes:
                        field_desc += '  # ' + ' '.join(comment_notes)
                    yield '    %s' % field_desc
                is_view = any(info.name == table_name and info.type == 'v' for info in table_info)
                is_partition = any(info.name == table_name and info.type == 'p' for info in table_info)
                for meta_line in self.get_meta(table_name, constraints, column_to_field_name, is_view, is_partition):
                    yield meta_line
                yield '        app_label = %r' % app_label
