import logging
import os

from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

from admin_extra_buttons.decorators import button
from admin_extra_buttons.mixins import ExtraButtonsMixin
from adminactions.mass_update import mass_update
from constance import config
from strategy_field.utils import fqn

from unicef_rest_framework import acl
from unicef_rest_framework.forms import ServiceForm
from unicef_rest_framework.models import Service

logger = logging.getLogger(__name__)

ACL_ICONS = {acl.ACL_ACCESS_OPEN: ('icon-angry', 'red'),
             acl.ACL_ACCESS_LOGIN: ('icon-smile', 'orange'),
             acl.ACL_ACCESS_RESTRICTED: ('icon-evil', 'green'),
             acl.ACL_ACCESS_RESERVED: ('icon-frustrated', 'black'),
             }


def get_stash_url(obj, label=None, **kwargs):
    if not obj:
        return ''
    qn = fqn(obj)
    url = "{}{}.py".format(config.SOURCE_REPOSITORY,
                           os.path.dirname(qn.replace('.', '/')))
    attrs = " ".join(['{}="{}"'.format(k, v) for k, v in kwargs.items()])
    return mark_safe('<a class="code" {} href="{}?c={}">{}</a>'.format(attrs,
                                                                       url,
                                                                       qn,
                                                                       label or qn.split('.')[-1]))


class ServiceAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ('short_name', 'visible', 'access', 'cache_version', 'suffix', 'json', 'admin')
    list_filter = ('hidden', 'access')

    search_fields = ('name', 'viewset')
    readonly_fields = ('cache_version', 'cache_ttl', 'cache_key', 'viewset', 'name', 'uuid',
                       'last_modify_user', 'source_model', 'endpoint', 'basename', 'suffix')
    form = ServiceForm
    mass_update_hints = []
    mass_update_exclude = ['linked_models', 'source_model', 'viewset', 'suffix', 'name',
                           'version']
    filter_horizontal = ('linked_models',)
    fieldsets = [("", {"fields": ('name',
                                  'description',
                                  ('access', 'hidden',),
                                  # 'confidentiality',
                                  ('source_model', 'basename'),
                                  ('suffix', 'endpoint'),
                                  'linked_models',
                                  )})]
    actions = [mass_update, ]

    # change_list_template = 'admin/unicef_rest_framework/service/change_list.html'

    def has_add_permission(self, request):
        return False

    def sourcecode(self, object):
        url = reverse("admin:unicef_rest_framework_service_source", args=[object.pk])
        return mark_safe('<a href="{}">code</a>'.format(url))

    sourcecode.allow_tags = True
    sourcecode.short_description = 'sourcecode'

    def acl_page(self, object):
        url = reverse("admin:unicef_rest_framework_service_acl", args=[object.pk])
        return mark_safe('<a href="{}">acl</a>'.format(url))

    acl_page.allow_tags = True
    acl_page.short_description = 'ACL'

    def short_name(self, obj):
        return "%s.%s" % (obj.source_model.app_label, obj.source_model.model)

    def security(self, object):

        return mark_safe('<i title="{}" '
                         'class="icon {}" '
                         'style="color: {};font-size:14pt"></i>'.format(object.get_access_display(),
                                                                        *ACL_ICONS[object.access]))

    security.allow_tags = True

    def json(self, obj):
        if obj.endpoint:
            return mark_safe("<a href='{}' target='a'>api</a>".format(obj.endpoint))
        else:
            return ''

    json.allow_tags = True
    json.short_description = 'view'

    def admin(self, obj):
        if obj.managed_model:
            opts = obj.managed_model._meta
            try:
                admin_url = reverse(admin_urlname(opts, 'changelist'))
                return mark_safe("<a href='{}' target='a'>{}</a>".format(admin_url, opts.object_name))
            except NoReverseMatch:
                return mark_safe('<span class="error red">{}</span>'.format(opts.object_name))

        else:
            return ''

    admin.allow_tags = True
    admin.short_description = 'model'

    def visible(self, obj):
        return not obj.hidden

    visible.boolean = True

    @button()
    def refresh(self, request):
        msgs = {False: 'No new services found',
                True: 'Found {} new services. Removed {}'}
        created, deleted, total = Service.objects.load_services()
        self.message_user(request, msgs[bool(created | deleted)].format(created, deleted))
        info = self.model._meta.app_label, self.model._meta.model_name
        return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % info))

    @button(label='Invalidate Cache')
    def invalidate_all_cache(self, request):
        Service.objects.invalidate_cache()

    @button()
    def doc(self, request, pk):
        service = Service.objects.get(pk=pk)
        return HttpResponseRedirect(service.doc_url())

    @button()
    def api(self, request, pk):
        service = Service.objects.get(pk=pk)
        return HttpResponseRedirect(service.endpoint)

    @button()
    def data(self, request, pk):
        service = Service.objects.get(pk=pk)
        model = service.managed_model
        url = reverse('admin:%s_%s_changelist' % (model._meta.app_label,
                                                  model._meta.model_name))
        return HttpResponseRedirect(url)

    @button()
    def invalidate_cache(self, request, pk):
        service = Service.objects.get(pk=pk)
        service.invalidate_cache()
        if request.is_ajax():
            return HttpResponse(service.cache_version, content_type='text/plain')
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # @button(visible=False)
    # def code(self, request, pk):
    #     cls = request.GET.get('c', None)
    #     if cls:
    #         target = import_by_name(cls)
    #     else:
    #         service = Service.objects.get(pk=pk)
    #         target = service.view
    #     code = inspect.getsource(target)
    #     return HttpResponse(code, content_type='text/plain')

    # def changelist_view(self, request, extra_context=None):
    #     return super().changelist_view(request, extra_context)
