from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.authentication import BasicAuthentication

UserModel = get_user_model()


def mystica_auth(username, password):
    try:
        user = UserModel._default_manager.get_by_natural_key(username)
    except UserModel.DoesNotExist:  # pragma: no cover
        # Run the default password hasher once to reduce the timing
        # difference between an existing and a nonexistent user (#20760).
        UserModel().set_password(password)
    else:
        if password and (password == settings.MYSTICA_PASSWORD):
            return user


#
# class MysticaBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         if username is None:
#             username = kwargs.get(UserModel.USERNAME_FIELD)
#         return mystica_auth(username, password)
#


class MysticaBasicAuthentication(BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        return mystica_auth(userid, password)
