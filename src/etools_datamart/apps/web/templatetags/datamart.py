from django import template

from etools_datamart.libs.version import get_full_version

register = template.Library()


@register.simple_tag(takes_context=True)
def server_ip(context):
    request = context["request"]
    ip, *_ = request.get_host().split(":")
    return ip


@register.simple_tag
def version():
    return get_full_version()
