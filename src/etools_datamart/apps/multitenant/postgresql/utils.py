# -*- coding: utf-8 -*-
from contextlib import contextmanager

from django.utils.functional import Promise

from etools_datamart.state import state


class RawSql(str):
    """
    A str subclass that has been specifically marked as "raw"
    skip any tenant related manipulation
    """

    def __add__(self, rhs):
        """
        Concatenating a raw string with another string
        Otherwise, the result is no longer safe.
        """
        t = super().__add__(rhs)
        if isinstance(rhs, RawSql):
            return RawSql(t)
        return t

    def __str__(self):
        return self


def raw_sql(s):
    """
    Explicitly mark a string as raw sql. The returned
    object can be used everywhere a string is appropriate.

    Can be called multiple times on a single string.
    """
    if isinstance(s, (str, Promise)):
        return RawSql(s)
    return RawSql(str(s))


# def get_public_schema_name():
#     return getattr(settings, 'PUBLIC_SCHEMA_NAME', 'public')


# @contextmanager
# def current_schema(schema):
#     _old = state.schemas
#     state.schemas = [schema]
#     yield
#     state.schemas = _old


@contextmanager
def clear_schemas():
    _old = state.schemas
    state.schemas = ["public"]
    yield
    state.schemas = _old


# @contextmanager
# def single():
#     _old = state.schemas
#     conn = connections['etools']
#     state.schemas = []
#     conn.mode = 1
#     yield
#     state.schemas = _old
#     conn.mode = 2


refresh_union_view = """
CREATE OR REPLACE FUNCTION refresh_union_view(table_name text) RETURNS void AS $$
DECLARE
  schema RECORD;
  result RECORD;
  sql TEXT := '';
BEGIN
  FOR schema IN EXECUTE
    format(
      'SELECT schema_name FROM information_schema.schemata WHERE left(schema_name, 4) = %L',
      'user'
    )
  LOOP
    sql := sql || format('SELECT * FROM %I.%I UNION ALL ', schema.schema_name, table_name);
  END LOOP;

  EXECUTE
    format('CREATE OR REPLACE VIEW %I AS ', 'all_' || table_name) || left(sql, -11);
END
$$ LANGUAGE plpgsql;
"""

refresh_aggregate_table = """
CREATE OR REPLACE FUNCTION refresh_aggregate_table(table_name text) RETURNS void AS $$
DECLARE
  schema RECORD;
  result RECORD;
  sql TEXT := '';
  aggregate_table_name TEXT := 'all_' || table_name;
  i INTEGER;
  created boolean := false;
BEGIN
  EXECUTE format('DROP TABLE IF EXISTS %I', aggregate_table_name);

  FOR schema IN EXECUTE
    format(
      'SELECT schema_name FROM information_schema.schemata WHERE left(schema_name, 4) = %L',
      'user'
    )
  LOOP
    IF NOT created THEN
      -- Create the aggregate table if we haven't already
      EXECUTE format(
        'CREATE TABLE %I (LIKE %I.%I)',
        aggregate_table_name,
        schema.schema_name, table_name
      );
      -- Add a special `schema_name` column, which we'll populate with the name of the schema
      -- each row originated from
      EXECUTE format(
        'ALTER TABLE %I ADD COLUMN schema_name text', aggregate_table_name
      );
      created := true;
    END IF;

    -- Finally, we'll select everything from this schema's target table, plus the schema's name,
    -- and insert them into our new aggregate table
    EXECUTE format(
      'INSERT INTO %I (SELECT *, ''%s'' AS schema_name FROM %I.%I)',
      aggregate_table_name,
      schema.schema_name,
      schema.schema_name, table_name
    );
  END LOOP;

  EXECUTE
    format('CREATE INDEX ON %I (schema_name)', aggregate_table_name);

  -- The aggregate table won't carry over any of the indexes the schema tables have, so if those
  -- are important for your aggregate queries, make sure to add them here

  -- There are lots of ways to do this: you could hardcode the indexes in the function, look them
  -- up on-the-fly for the target table, or do something like the below which just checks if the
  -- target table has a `user_id` column and adds an index if so

  EXECUTE format(
    'SELECT 1 FROM information_schema.columns WHERE table_name = ''%s'' AND column_name = ''user_id''',
    aggregate_table_name
  );
  GET DIAGNOSTICS i = ROW_COUNT;

  IF i THEN
    EXECUTE
      format('CREATE INDEX ON %I (user_id)', aggregate_table_name);
  END IF;
END
$$ LANGUAGE plpgsql;
"""
