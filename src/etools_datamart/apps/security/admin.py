from django.contrib import admin
from django.db import connections

from .forms import SchemaAccessControlForm
from .models import SchemaAccessControl

conn = connections['etools']


@admin.register(SchemaAccessControl)
class SchemaAccessControlAdmin(admin.ModelAdmin):
    form = SchemaAccessControlForm
    list_display = ('group', 'schemas')
