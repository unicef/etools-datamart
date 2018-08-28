# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import register
from django.http import HttpResponseRedirect
from django.urls import reverse
from humanize import naturaldelta

from . import models


@register(models.Execution)
class ExecutionAdmin(admin.ModelAdmin):
    list_display = readonly_fields = ('task', 'timestamp', 'result', 'time',
                                      'last_success', 'last_failure')
    date_hierarchy = 'timestamp'
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def time(self, obj):
        return naturaldelta(obj.elapsed)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if request.method == 'POST':
            redirect_url = reverse('admin:%s_%s_changelist' % (self.opts.app_label,
                                                               self.opts.model_name))
            return HttpResponseRedirect(redirect_url)
        return self._changeform_view(request, object_id, form_url, extra_context)
