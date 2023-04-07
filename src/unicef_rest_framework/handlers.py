import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

#
# @receiver(config_updated)
# def constance_updated(sender, key, old_value, new_value, **kwargs):
#     if key == 'SYSTEM_PASSWORD':
#
#     print(sender, key, old_value, new_value)


@receiver(post_migrate)
def create_system_user(app_config, **kwargs):
    from rest_framework.authtoken.models import Token

    uname = os.environ.get("SYSTEM_USER", "system")
    ModelUser = get_user_model()
    user, __ = ModelUser.objects.get_or_create(username=uname, defaults={"is_superuser": True, "is_staff": False})

    Token.objects.get_or_create(user=user)
