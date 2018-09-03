# -*- coding: utf-8 -*-
from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def select_schema(context):
    url = reverse("select-schema")
    request = context['request']
    return f"{url}?from={request.path}"
