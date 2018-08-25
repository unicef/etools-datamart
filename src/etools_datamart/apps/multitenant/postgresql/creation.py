import subprocess
import sys
from pathlib import Path

from django.conf import settings
from django.db.backends.postgresql_psycopg2 import creation as original_creation

from etools_datamart.apps.multitenant.postgresql.utils import raw_sql


class DatabaseCreation(original_creation.DatabaseCreation):

    # def _quote_name(self, name):
    #     raise NotImplementedError
    #     return self.connection.ops.quote_name(name)

    def _create_test_db(self, verbosity, autoclobber, keepdb=False):
        """
        Internal implementation - create the test db tables.
        """
        test_database_name = self._get_test_db_name()
        test_db_params = {
            'dbname': self.connection.ops.quote_name(test_database_name),
            'suffix': self.sql_table_creation_suffix(),
        }
        # Create the test database and connect to it.
        with self._nodb_connection.cursor() as cursor:
            try:
                self._execute_create_test_db(cursor, test_db_params, keepdb)
            except Exception as e:
                # if we want to keep the db, then no need to do any of the below,
                # just return and skip it all.
                if keepdb:
                    return test_database_name

                sys.stderr.write(
                    "Got an error creating the test database: %s\n" % e)
                if not autoclobber:
                    confirm = input(
                        "Type 'yes' if you would like to try deleting the test "
                        "database '%s', or 'no' to cancel: " % test_database_name)
                if autoclobber or confirm == 'yes':
                    try:
                        if verbosity >= 1:
                            print("Destroying old test database for alias %s..." % (
                                self._get_database_display_str(verbosity, test_database_name),
                            ))
                        cursor.execute(raw_sql('DROP DATABASE %(dbname)s' % test_db_params))
                        self._execute_create_test_db(cursor, test_db_params, keepdb)
                    except Exception as e:
                        sys.stderr.write(
                            "Got an error recreating the test database: %s\n" % e)
                        sys.exit(2)
                else:
                    print("Tests cancelled.")
                    sys.exit(1)

        return test_database_name

    def create_test_db(self, verbosity=1, autoclobber=False, serialize=True, keepdb=False):
        """
        Create a test database, prompting the user for confirmation if the
        database already exists. Return the name of the test database created.
        """
        # Don't import django.core.management if it isn't needed.

        test_database_name = self._get_test_db_name()
        if verbosity >= 1:
            action = 'Creating'
            if keepdb:
                action = "Using existing"

            print("%s test database for alias %s..." % (
                action,
                self._get_database_display_str(verbosity, test_database_name),
            ))

        # We could skip this call if keepdb is True, but we instead
        # give it the keepdb param. This is to handle the case
        # where the test DB doesn't exist, in which case we need to
        # create it, then just not destroy it. If we instead skip
        # this, we will get an exception.
        self._create_test_db(verbosity, autoclobber, keepdb)

        self.connection.close()
        settings.DATABASES[self.connection.alias]["NAME"] = test_database_name
        self.connection.settings_dict["NAME"] = test_database_name
        if keepdb:
            return

        cur = self.connection.cursor()
        cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA pg_catalog;")

        header = """
CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA {schema};
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA {schema};
CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA {schema};
SET default_tablespace = '';
"""

        cmds = ["pg_restore",
                "-U", self.connection.settings_dict['USER'],
                "-p", str(self.connection.settings_dict['PORT']),
                "-h", self.connection.settings_dict['HOST'],
                "-d", self.connection.settings_dict['NAME'],
                "--no-owner",
                "--disable-triggers",
                "--exit-on-error",
                str(Path(__file__).parent / "public.sqldump")]

        subprocess.check_call(cmds)

        try:
            cur.execute(raw_sql(header.format(schema='public')))
        except Exception as e:
            raise Exception(f"Error creating schema 'public'") from e

        for schema in settings.TEST_SCHEMAS:
            try:
                sql = (Path(__file__).parent / f'tenant.sql').read_text()
                sql = sql.replace("[[schema]]", schema).replace("SET default_tablespace = '';",
                                                                header.format(schema=schema))
                cur.execute(raw_sql(sql))
            except Exception as e:
                raise Exception(f"Error creating schema {schema}") from e

        self.connection.ensure_connection()

        return test_database_name

    # def destroy_test_db(self, old_database_name=None, verbosity=1, keepdb=False, suffix=None):
    #     raise NotImplementedError
    #     super().destroy_test_db(old_database_name, verbosity, keepdb, suffix)
    #
    # def _get_database_create_suffix(self, encoding=None, template=None):
    #     raise NotImplementedError
    #     suffix = ""
    #     if encoding:
    #         suffix += " ENCODING '{}'".format(encoding)
    #     if template:
    #         suffix += " TEMPLATE {}".format(self._quote_name(template))
    #     if suffix:
    #         suffix = "WITH" + suffix
    #     return suffix
    #
    # def sql_table_creation_suffix(self):
    #     test_settings = self.connection.settings_dict['TEST']
    #     assert test_settings['COLLATION'] is None, (
    #         "PostgreSQL does not support collation setting at database creation time."
    #     )
    #     return self._get_database_create_suffix(
    #         encoding=test_settings['CHARSET'],
    #         template=test_settings.get('TEMPLATE'),
    #     )
    #
    # def _execute_create_test_db(self, cursor, parameters, keepdb=False):
    #     raise NotImplementedError
    #     try:
    #         super()._execute_create_test_db(cursor, parameters, keepdb)
    #     except Exception as e:
    #         if getattr(e.__cause__, 'pgcode', '') != errorcodes.DUPLICATE_DATABASE:
    #             # All errors except "database already exists" cancel tests.
    #             sys.stderr.write('Got an error creating the test database: %s\n' % e)
    #             sys.exit(2)
    #         elif not keepdb:
    #             # If the database should be kept, ignore "database already
    #             # exists".
    #             raise e

    def _execute_create_test_db(self, cursor, parameters, keepdb=False):
        cursor.execute(raw_sql('CREATE DATABASE %(dbname)s %(suffix)s' % parameters))
        try:
            cursor.execute(raw_sql('CREATE ROLE etoolusr'))
        except Exception:
            pass

    def _clone_test_db(self, suffix, verbosity, keepdb=False):
        raise NotImplementedError
