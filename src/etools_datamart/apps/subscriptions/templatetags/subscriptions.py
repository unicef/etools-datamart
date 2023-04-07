from django import template

from etools_datamart.apps.subscriptions.models import Subscription

register = template.Library()


@register.inclusion_tag("subscription_select.html", takes_context=True)
def subscription_select(context, task):
    user = context["user"]
    s = Subscription.objects.filter(content_type=task.content_type, kwargs="", user=user).first()
    return {"options": Subscription.TYPES, "task": task, "subscription": s}
