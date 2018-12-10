import collections

from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag
def build_query(**kwargs):
    """Build a query string"""
    query_dict = QueryDict(mutable=True)

    for k, v in kwargs.items():
        if isinstance(v, collections.Iterable) and not isinstance(v, str):
            query_dict.setlist(k, v)
        else:
            query_dict[k] = v

    return query_dict.urlencode()


@register.simple_tag(takes_context=True)
def set_query_values(context, **kwargs):
    """Override existing parameters in the current query string"""
    query_dict = context.request.GET.copy()

    for k, v in kwargs.items():
        if isinstance(v, collections.Iterable) and not isinstance(v, str):
            query_dict.setlist(k, v)
        else:
            query_dict[k] = v

    return query_dict.urlencode()


@register.simple_tag(takes_context=True)
def append_query_values(context, **kwargs):
    """Append to existing parameters in the current query string"""
    query_dict = context.request.GET.copy()

    for k, v in kwargs.items():
        if isinstance(v, collections.Iterable) and not isinstance(v, str):
            for v_item in v:
                query_dict.appendlist(k, v_item)
        else:
            query_dict.appendlist(k, v)

    return query_dict.urlencode()
