from django.forms import ChoiceField, forms
from django.template import loader

import coreapi
import coreschema
from dynamic_serializer.core import DynamicSerializerMixin as DynamicSerializerMixinBase
from rest_framework.filters import BaseFilterBackend


class DynamicSerializerMixin(DynamicSerializerMixinBase):
    def get_selected_serializer_name(self):
        return self.request.query_params.get(self.serializer_field_param, 'std')


class SchemaSerializerField(coreschema.Enum):

    def __init__(self, view: DynamicSerializerMixin, **kwargs):
        self.view = view
        kwargs.setdefault('title', 'serializers')
        kwargs.setdefault('description', self.build_description())
        super().__init__(list(view.serializers_fieldsets.keys()), **kwargs)

    def build_description(self):
        defs = []
        names = []
        for k, v in self.view.serializers_fieldsets.items():
            names.append(k)
            defs.append(f"""- **{k}**: {self.view.get_serializer_fields(k)}
""")

        description = f"""Define the set of fields to return. Allowed values are:
            [{'*, *'.join(names)}*]

{''.join(defs)}
        """
        return description


class DynamicSerializerFilter(BaseFilterBackend):
    # template = 'rest_framework/filters/search.html'
    ordering_title = 'Serializer'
    template = 'dynamic_serializer/select.html'

    def get_schema_fields(self, view):
        ret = []
        if view.serializers_fieldsets:
            ret.append(coreapi.Field(
                name=view.serializer_field_param,
                required=False,
                location='query',
                schema=SchemaSerializerField(view)
            ))
        return ret

    def filter_queryset(self, request, queryset, view):
        return queryset

    def get_form(self, request, view):
        choices = zip(view.serializers_fieldsets.keys(), view.serializers_fieldsets.keys())
        Frm = type("SerializerForm", (forms.Form,),
                   {view.serializer_field_param: ChoiceField(
                       label="Serializer",
                       choices=choices,
                       required=False)})
        return Frm(request.GET)

    def get_template_context(self, request, queryset, view):
        current = view.get_selected_serializer_name()
        context = {'request': request,
                   'current': current,
                   'form': self.get_form(request, view),
                   'param': view.serializer_field_param,
                   }
        context['options'] = view.serializers_fieldsets.keys()
        return context

    def to_html(self, request, queryset, view):
        if len(view.serializers_fieldsets.keys()) > 1:
            template = loader.get_template(self.template)
            context = self.get_template_context(request, queryset, view)
            return template.render(context)
