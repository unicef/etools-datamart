from rest_framework.metadata import SimpleMetadata


def get_create_model(editor, model):  # pragma: no cover
    """
    Create a table and any accompanying indexes or unique constraints for
    the given `model`.
    """
    # Create column SQL, add FK deferreds if needed
    column_sqls = []
    params = []
    for field in model._meta.local_fields:
        # SQL
        definition, extra_params = editor.column_sql(model, field)
        if definition is None:
            continue
        # Check constraints can go on the column SQL here
        db_params = field.db_parameters(connection=editor.connection)
        if db_params['check']:
            definition += " CHECK (%s)" % db_params['check']
        # Autoincrement SQL (for backends with inline variant)
        col_type_suffix = field.db_type_suffix(connection=editor.connection)
        if col_type_suffix:
            definition += " %s" % col_type_suffix
        params.extend(extra_params)
        # FK
        if field.remote_field and field.db_constraint:
            to_table = field.remote_field.model._meta.db_table
            to_column = field.remote_field.model._meta.get_field(field.remote_field.field_name).column
            if editor.sql_create_inline_fk:
                definition += " " + editor.sql_create_inline_fk % {
                    "to_table": editor.quote_name(to_table),
                    "to_column": editor.quote_name(to_column),
                }
            elif editor.connection.features.supports_foreign_keys:
                editor.deferred_sql.append(editor._create_fk_sql(model, field, "_fk_%(to_table)s_%(to_column)s"))
        # Add the SQL to our big list
        column_sqls.append("%s %s" % (
            editor.quote_name(field.column),
            definition,
        ))
        # Autoincrement SQL (for backends with post table definition variant)
        if field.get_internal_type() in ("AutoField", "BigAutoField"):
            autoinc_sql = editor.connection.ops.autoinc_sql(model._meta.db_table, field.column)
            if autoinc_sql:
                editor.deferred_sql.extend(autoinc_sql)

    # Add any unique_togethers (always deferred, as some fields might be
    # created afterwards, like geometry fields with some backends)
    for fields in model._meta.unique_together:
        columns = [model._meta.get_field(field).column for field in fields]
        editor.deferred_sql.append(editor._create_unique_sql(model, columns))
    # Make the table
    sql = editor.sql_create_table % {
        "table": editor.quote_name(model._meta.db_table),
        "definition": ", ".join(column_sqls)
    }
    if model._meta.db_tablespace:
        tablespace_sql = editor.connection.ops.tablespace_sql(model._meta.db_tablespace)
        if tablespace_sql:
            sql += ' ' + tablespace_sql
    return sql


class SimpleMetadataWithFilters(SimpleMetadata):
    """Override SimpleMetadata, adding info about filters"""

    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        metadata['filters'] = getattr(view, 'filter_fields', '')
        metadata['filter_blacklist'] = getattr(view, 'filter_blacklist', '')
        metadata['ordering'] = getattr(view, 'ordering_fields', '')
        if hasattr(view, 'serializers_fieldsets'):
            metadata['serializers'] = ", ".join(view.serializers_fieldsets.keys())
        else:  # pragma: no cover
            metadata['serializers'] = 'std'

            # from django.db import connection
        # with connection.schema_editor() as editor:
        #     sql = get_create_model(editor, view.queryset.model)
        # metadata['sql'] = sql

        return metadata
