# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def server_ip(context):
    request = context['request']
    ip, *_ = request.get_host().split(":")
    return ip
