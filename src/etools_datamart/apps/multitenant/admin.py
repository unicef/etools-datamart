# -*- coding: utf-8 -*-
from admin_extra_urls.extras import ExtraUrlMixin
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse

from etools_datamart.state import state


class TenantChangeList(ChangeList):
    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        return reverse('admin:%s_%s_change' % (self.opts.app_label,
                                               self.opts.model_name),
                       args=[quote(f"{pk}-{ result.schema}")],
                       current_app=self.model_admin.admin_site.name)


# def format_stm(stm):
#     return sqlparse.format(str(stm),
#                            keyword_case="upper",
#                            reindent=True,
#                            indent_width=4,
#                            wrap_after=80)


class TenantModelAdmin(ExtraUrlMixin, ModelAdmin):
    actions = None
    # list_filter = ('schema',)

    def get_queryset(self, request):
        # if state.get("query"):
        #     return self.model._default_manager.raw(state.get("query"))
        return super().get_queryset(request)

    # @link(label='Raw SQL')
    # def raw_sql(self, request):
    #     opts = self.model._meta
    #     context = dict(app_label=opts.app_label,
    #                    opts=opts,
    #                    state=state)
    #     if request.method == 'POST':
    #         form = SQLForm(data=request.POST)
    #
    #         if form.is_valid():
    #             if 'submit' in request.POST:
    #                 if form.cleaned_data['raw']:
    #                     sql = original = form.cleaned_data['statement']
    #                 else:
    #                     p = Parser(form.cleaned_data['statement'])
    #                     original = p.original
    #                     sql = format_stm(p.with_schemas(*state.schemas))
    #
    #                 form = SQLForm(confirm=True,
    #                                initial={'statement': sql,
    #                                         'original': original,
    #                                         'raw': form.cleaned_data['raw']
    #                                         })
    #                 context['statement'] = sql
    #
    #             elif 'back' in request.POST:
    #                 form = SQLForm(initial={'statement': form.cleaned_data['original'],
    #                                         'original': ""
    #                                         })
    #             elif 'doit' in request.POST:
    #                 try:
    #                     if form.cleaned_data['raw']:
    #                         stm = raw_sql(clean_stm(form.cleaned_data['statement']))
    #                     else:
    #                         stm = clean_stm(form.cleaned_data['statement'])
    #                     conn = connections['etools']
    #                     cur = conn.cursor()
    #                     cur.execute(stm)
    #                     cur.fetchone()
    #                     # data = self.model._default_manager.raw(raw_sql(stm))
    #                     # assert data
    #                 except Exception as e:
    #                     form = SQLForm(initial={'statement': form.cleaned_data['original'],
    #                                             'original': ""
    #                                             })
    #                     self.message_user(request, str(e), messages.ERROR)
    #                 else:
    #                     state.set("query", form.cleaned_data['statement'])
    #                     return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))
    #         else:
    #             pass
    #     else:
    #         qs = self.model._default_manager.get_queryset().defer("schema")
    #         form = SQLForm(initial={'statement': format_stm(str(qs.query))})
    #
    #     context['form'] = form
    #     return TemplateResponse(request,
    #                             'raw_sql.html',
    #                             context=context)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_object(self, request, object_id, from_field=None):
        pk, schema = object_id.split('-')
        queryset = self.get_queryset(request)
        model = queryset.model
        field = model._meta.pk if from_field is None else model._meta.get_field(from_field)
        try:
            pk = field.to_python(pk)
            state.schemas = [schema]
            return queryset.get(**{field.name: pk})
        except MultipleObjectsReturned:  # pragma: no cover
            raise
        except (model.DoesNotExist, ValidationError, ValueError):  # pragma: no cover
            return None

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if request.method == 'POST':
            redirect_url = reverse('admin:%s_%s_changelist' % (self.opts.app_label,
                                                               self.opts.model_name))

            self.message_user(request, "This admin is read-only. Record not saved.", level=messages.WARNING)
            return HttpResponseRedirect(redirect_url)
        return self._changeform_view(request, object_id, form_url, extra_context)

    def get_changelist(self, request, **kwargs):
        return TenantChangeList
