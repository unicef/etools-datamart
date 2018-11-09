# -*- coding: utf-8 -*-
from django import template
from django.db import connections

from etools_datamart.state import state

register = template.Library()

#
# @register.simple_tag(takes_context=True)
# def select_schema(context):
#     url = reverse("select-schema")
#     request = context['request']
#     return f"{url}?from={request.path}"


@register.simple_tag(takes_context=True)
def schemas(context):
    conn = connections['etools']
    context['schemas'] = conn.schemas
    return ""


@register.simple_tag(takes_context=True)
def get_state(context):
    context['state'] = state
    context['request'] = state.request
    return ""
