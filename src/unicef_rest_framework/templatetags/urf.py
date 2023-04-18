import logging

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

import six
from strategy_field.utils import fqn

from unicef_rest_framework.admin.service import ACL_ICONS
from unicef_rest_framework.utils import humanize_size

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter()
def doc(api):
    return api.__doc__


@register.filter()
def humanize(value):
    if value:
        return humanize_size(value)
    return ""


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, "")


@register.filter(name="fqn")
def _fqn(obj):
    if obj:
        return fqn(obj)


@register.simple_tag(takes_context=True)
def code(context, obj):
    if not obj:
        return ""
    elif isinstance(obj, (list, tuple)):
        return ", ".join(obj)
    elif isinstance(obj, six.string_types):
        return obj
    service = context["service"]
    qn = fqn(obj)
    # return qn
    url = reverse("admin:unicef_rest_framework_service_code", args=[service.pk])
    return mark_safe('<a class ="code" href="{}?c={}">{}</a>'.format(url, qn, qn.split(".")[-1]))


@register.simple_tag(takes_context=True)
def acl_icon(context, obj, _as=None, _var=None):
    icon = ACL_ICONS[obj.access]
    if _as:
        context[_var] = icon

    return icon
