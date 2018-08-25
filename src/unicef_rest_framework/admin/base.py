# -*- coding: utf-8 -*-

import logging

from admin_extra_urls.extras import ExtraUrlMixin, link
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse

logger = logging.getLogger(__name__)


class ReadOnlyModelAdmin(object):
    editing = False

    def get_readonly_fields(self, request, obj=None):
        if self.editing:
            return self.readonly_fields
        return [f.name for f in self.model._meta.fields]


class TruncateTableMixin(ExtraUrlMixin):
    truncate_cascade = False

    def has_delete_permission(self, request, obj=None):
        return True

    @link(label='Empty Table', css_class="btn btn-danger", icon="fa fa-warning icon-white")
    def empty_log(self, request):
        opts = self.model._meta
        context = dict(
            self.admin_site.each_context(request),
            opts=opts,
            app_label=opts.app_label,
        )
        if request.method == 'POST':
            from django.db import connection

            cascade = {True: 'CASCADE', False: ''}
            cursor = connection.cursor()
            cursor.execute('TRUNCATE TABLE "{1}" {0}'.format(cascade[self.truncate_cascade],
                                                             self.model._meta.db_table))
            return HttpResponseRedirect(reverse(admin_urlname(opts,
                                                              'changelist')))

        return TemplateResponse(request,
                                'admin/unicef_rest_framework/confirm_truncate.html',
                                context)


class ListDisplayAllMixin(object):
    list_display = ()
    list_display_exclude = ('id', 'uuid', 'version',
                            'last_modified_user', 'last_modified_date')

    def get_list_display(self, request):
        if not self.list_display:
            return [f.name for f in self.model._meta.fields
                    if f.name not in self.list_display_exclude]
        return self.list_display


class APIModelAdmin(ListDisplayAllMixin, ReadOnlyModelAdmin,
                    admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

        # def has_change_permission(self, request, obj=None):
        # return obj is None
