# -*- coding: utf-8 -*-
from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def server_ip(context):
    request = context['request']
    ip, *_ = request.get_host().split(":")
    return ip
