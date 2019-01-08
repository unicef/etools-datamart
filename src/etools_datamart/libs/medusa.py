from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from rest_framework.authentication import BasicAuthentication

UserModel = get_user_model()


def medusa_auth(username, password):
    try:
        user = UserModel._default_manager.get_by_natural_key(username)
    except UserModel.DoesNotExist:
        # Run the default password hasher once to reduce the timing
        # difference between an existing and a nonexistent user (#20760).
        UserModel().set_password(password)
    else:
        if password and (password == settings.MEDUSA_PASSWORD):
            return user


class MedusaBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        return medusa_auth(username, password)


class MedusaBasicAuthentication(BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        return medusa_auth(userid, password)
