from django import forms

from rest_framework.filters import OrderingFilter as OrderingFilterBase


class OrderingFilter(OrderingFilterBase):
    template = 'rest_framework/filters/filter_form.html'

    def get_form(self, request, view, context):
        Frm = type("OrderForm", (forms.Form,),
                   {context['param']: forms.ChoiceField(
                       label="Ordering",
                       choices=context['options'],
                       required=False)})
        return Frm(request.GET)

    def get_template_context(self, request, queryset, view):
        context = super().get_template_context(request, queryset, view)
        context['form'] = self.get_form(request, view, context)
        return context
