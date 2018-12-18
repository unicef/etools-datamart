from django.contrib import admin

from etools_datamart.apps.security.models import SchemaAccessControl


@admin.register(SchemaAccessControl)
class SchemaAccessControlAdmin(admin.ModelAdmin):
    list_display = ('group', 'schemas')
