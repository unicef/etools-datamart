import logging

from constance import config
from crashlog.middleware import process_exception
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework_jwt import authentication
from unicef_security.azure import default_group, Synchronizer

logger = logging.getLogger()


def jwt_get_username_from_payload(payload):
    return payload.get('preferred_username')


class JWTAuthentication(authentication.JSONWebTokenAuthentication):
    def authenticate(self, request):

        jwt_value = self.get_jwt_value(request)

        if jwt_value is None:  # pragma: no cover
            return None

        try:
            user, jwt_value = super(JWTAuthentication, self).authenticate(request)
        except TypeError:  # pragma: no cover
            raise PermissionDenied(detail='No valid authentication provided')
        except AuthenticationFailed as e:  # pragma: no cover
            raise PermissionDenied(detail='JWT Authentication Failed: %s' % e)
        return user, jwt_value

    def authenticate_credentials(self, payload):
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)
        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)
        created = False
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            if config.AZURE_USE_GRAPH:
                try:
                    s = Synchronizer()
                    user_info = s.get_user(username)
                    pk, values = s.get_record(user_info)
                    user, created = User.objects.update_or_create(**pk,
                                                         defaults=values)
                except Exception as e:
                    process_exception(e)
                    raise exceptions.AuthenticationFailed("Unable to retrieve user data")
            else:
                user, created = User.objects.update_or_create(username=username,
                                                         email=username)
            if created:
                default_group(user=user, is_new=created)
        except Exception as e:
            logger.exception(e)
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user
