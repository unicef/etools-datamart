import logging
import re
from contextlib import contextmanager
from functools import lru_cache
from time import time

import django.db.utils
import psycopg2
from django.apps import apps
from django.conf import settings
from django.db.backends.postgresql import base as original_backend
from django.db.backends.utils import CursorWrapper
from django.utils.functional import cached_property

# from etools_datamart.state import state
from etools_datamart.apps.multitenant.exceptions import InvalidSchema

from ..sql import Parser
from .creation import DatabaseCreation
from .introspection import DatabaseSchemaIntrospection
from .utils import raw_sql, RawSql

EXTRA_SEARCH_PATHS = getattr(settings, 'PG_EXTRA_SEARCH_PATHS', [])

# from the postgresql doc
SQL_IDENTIFIER_RE = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]{,62}$')
SQL_SCHEMA_NAME_RESERVED_RE = re.compile(r'^pg_', re.IGNORECASE)

dj_logger = logging.getLogger('django.db.backends')
logger = logging.getLogger(__name__)


# SINGLE_TENANT = 1
# MULTI_TENANT = 2


# def _is_valid_identifier(identifier):
#     return bool(SQL_IDENTIFIER_RE.match(identifier))
#
#
# def _check_identifier(identifier):
#     if not _is_valid_identifier(identifier):
#         raise ValidationError("Invalid string used for the identifier.")
#
#
# def _is_valid_schema_name(name):
#     return _is_valid_identifier(name) and not SQL_SCHEMA_NAME_RESERVED_RE.match(name)
#
#
# def _check_schema_name(name):
#     if not _is_valid_schema_name(name):
#         raise ValidationError("Invalid string used for the schema name.")
#

class TenantCursor(CursorWrapper):

    # def fetchall(self):
    #     with self.db.wrap_database_errors:
    #         return self.cursor.fetchall()

    def execute(self, sql, params=None):
        if isinstance(sql, RawSql):
            return super(TenantCursor, self).execute(sql, params)
        msg = f"""
schemas: {self.db.schemas}

sql: {sql}
"""
        try:
            if len(self.db.schemas) == 0:
                return super(TenantCursor, self).execute(sql, params)
            # if not sql.strip().startswith('SELECT'):
            #     return super(TenantCursor, self).execute(sql, params)

            p = Parser(sql)
            tenant_sql = p.with_schemas(*self.db.schemas)
            msg = f"""

schemas: {self.db.schemas}

sql: {sql}

tenant: {tenant_sql}
"""

            logger.debug(msg)
            return super(TenantCursor, self).execute(tenant_sql, params * len(self.db.schemas))
        except django.db.utils.ProgrammingError as e:  # pragma: no cover
            logger.error(f"{e} {msg}")
            raise django.db.utils.ProgrammingError(f"{e} {msg}") from e
        except Exception as e:  # pragma: no cover
            logger.error(f"{e} {msg}")
            raise Exception(msg) from e


class TenantDebugCursor(TenantCursor):  # pragma: no cover
    def execute(self, sql, params=None):
        start = time()
        try:
            return super().execute(sql, params)
        finally:
            stop = time()
            duration = stop - start
            sql = self.db.ops.last_executed_query(self.cursor, sql, params)
            self.db.queries_log.append({
                'sql': sql,
                'time': "%.3f" % duration,
            })
            dj_logger.debug(
                '(%.3f) %s; args=%s', duration, sql, params,
                extra={'duration': duration, 'sql': sql, 'params': params}
            )

    # def executemany(self, sql, param_list):
    #     start = time()
    #     try:
    #         return super().executemany(sql, param_list)
    #     finally:
    #         stop = time()
    #         duration = stop - start
    #         try:
    #             times = len(param_list)
    #         except TypeError:  # param_list could be an iterator
    #             times = '?'
    #         self.db.queries_log.append({
    #             'sql': '%s times: %s' % (times, sql),
    #             'time': "%.3f" % duration,
    #         })
    #         dj_logger.debug(
    #             '(%.3f) %s; args=%s', duration, sql, param_list,
    #             extra={'duration': duration, 'sql': sql, 'params': param_list}
    #         )


class DatabaseWrapper(original_backend.DatabaseWrapper):
    """
    Adds the capability to manipulate the search_path using set_tenant and set_schema_name
    """
    include_public_schema = True
    creation_class = DatabaseCreation
    introspection_class = DatabaseSchemaIntrospection

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)

        # Use a patched version of the DatabaseIntrospection that only returns the table list for the
        # currently selected schema.
        self._schemas = []
        self.search_path_set = False
        # self.tenants = []

    def close(self):
        self.search_path_set = False
        self._schemas = []
        super(DatabaseWrapper, self).close()

    @property
    def schemas(self):
        return self._schemas

    @contextmanager
    def noschema(self):
        old = self.schemas
        self.set_schemas([])
        yield
        self.set_schemas(old)

    @lru_cache()
    def get_tenants(self):
        model = apps.get_model(settings.TENANT_MODEL)
        return model.objects.filter(**settings.SCHEMA_FILTER).exclude(**settings.SCHEMA_EXCLUDE).order_by('name')

    @cached_property
    def all_schemas(self):
        return set([c.schema_name for c in self.get_tenants()])

    def set_schemas(self, schemas):
        """
        Main API method to current database schema,
        but it does not actually modify the db connection.
        """
        def _validate(n):
            name = n.lower()
            if name not in self.all_schemas:
                raise InvalidSchema(n)
            return name

        self._schemas = sorted([_validate(s) for s in schemas])

        self.search_path_set = False

    def set_all_schemas(self):
        """
        Main API method to current database schema,
        but it does not actually modify the db connection.
        """
        self._schemas = self.all_schemas
        self.search_path_set = False

    # def set_schema(self, schema_name, include_public=True):
    #     """
    #     Main API method to current database schema,
    #     but it does not actually modify the db connection.
    #     """
    #     # self.tenant = FakeTenant(schema_name=schema_name)
    #     self.schema_name = schema_name
    #     self.include_public_schema = include_public
    #     # self.set_settings_schema(schema_name)
    #     self.search_path_set = False

    # def set_schema_to_public(self):
    #     """
    #     Instructs to stay in the common 'public' schema.
    #     """
    # self.tenant = FakeTenant(schema_name=get_public_schema_name())
    # self.schema_name = get_public_schema_name()
    # self.set_settings_schema(self.schema_name)
    # self.search_path_set = False

    # def set_settings_schema(self, schema_name):
    #     self.settings_dict['SCHEMA'] = schema_name

    # def get_schema(self):
    #     warnings.warn("connection.get_schema() is deprecated, use connection.schema_name instead.",
    #                   category=DeprecationWarning)
    #     return self.schema_name

    # def get_tenant(self):
    #     warnings.warn("connection.get_tenant() is deprecated, use connection.tenant instead.",
    #                   category=DeprecationWarning)
    #     return self.tenant

    def make_debug_cursor(self, cursor):  # pragma: no cover
        """Create a cursor that logs all queries in self.queries_log."""
        return TenantDebugCursor(cursor, self)

    def make_cursor(self, cursor):
        """Create a cursor without debug logging."""
        return TenantCursor(cursor, self)

    # def single_cursor(self, name=None, ):
    #     if name:
    #         # Only supported and required by Django 1.11 (server-side cursor)
    #         cursor = super(DatabaseWrapper, self)._cursor(name=name)
    #     else:
    #         cursor = super(DatabaseWrapper, self)._cursor()
    #     return cursor

    # def set_search_paths(self, cursor, *schemas):
    #     # state.schema = schemas
    #     cursor.execute(raw_sql('SET search_path = {0}'.format(','.join(schemas))))
    #     self.search_path_set = True

    # def clear_search_paths(self, cursor):
    #     # state.schemas = []
    #     cursor.execute(raw_sql('SET search_path = public;'))
    #     self.search_path_set = False

    def _cursor(self, name=None):
        """
        Here it happens. We hope every Django db operation using PostgreSQL
        must go through this to get the cursor handle. We change the path.
        """

        if name:  # pragma: no cover
            # Only supported and required by Django 1.11 (server-side cursor)
            cursor = super(DatabaseWrapper, self)._cursor(name=name)
        else:
            cursor = super(DatabaseWrapper, self)._cursor()

        # optionally limit the number of executions - under load, the execution
        # of `set search_path` can be quite time consuming

        if not self.search_path_set and self._schemas:
            search_paths = ["public"]
            search_paths.extend(self._schemas)
            if name:  # pragma: no cover
                # Named cursor can only be used once
                cursor_for_search_path = self.connection.cursor()
            else:
                # Reuse
                cursor_for_search_path = cursor
            # In the event that an error already happened in this transaction and we are going
            # to rollback we should just ignore database error when setting the search_path
            # if the next instruction is not a rollback it will just fail also, so
            # we do not have to worry that it's not the good one
            try:
                # self.set_search_paths(cursor_for_search_path, *search_paths)
                logger.debug(f"SET search_path: {search_paths}")
                cursor.execute(raw_sql('SET search_path = {0}'.format(','.join(search_paths))))
            except (django.db.utils.DatabaseError, psycopg2.InternalError):  # pragma: no cover
                self.search_path_set = False
            else:
                self.search_path_set = True

            if name:  # pragma: no cover
                cursor_for_search_path.close()

        return cursor

#
# class FakeTenant:
#     """
#     We can't import any db model in a backend (apparently?), so this class is used
#     for wrapping schema names in a tenant-like structure.
#     """
#
#     def __init__(self, schema_name):
#         self.schema_name = schema_name
