import base64
import logging

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from constance import config
from crashlog.middleware import process_exception
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework_jwt import authentication
from strategy_field.utils import fqn

from unicef_rest_framework import acl
from unicef_rest_framework.config import conf
from unicef_security.graph import default_group, Synchronizer

logger = logging.getLogger()


def jwt_get_username_from_payload(payload):
    return payload.get('preferred_username', payload.get('unique_name'))


def get_client_ip(environ):
    """
    Naively yank the first IP address in an X-Forwarded-For header
    and assume this is correct.

    Note: Don't use this in security sensitive situations since this
    value may be forged from a client.
    """
    try:
        return environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    except (KeyError, IndexError):
        return environ.get('REMOTE_ADDR')


class URLTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return None


class AnonymousAuthentication(BaseAuthentication):
    def authenticate(self, request):
        view = request._request._view
        service = view.get_service()
        if service.access == acl.ACL_ACCESS_OPEN:
            User = get_user_model()
            user = User.objects.get_or_create(username='anonymous')[0]
            request.user = user
            login(request, user, fqn(ModelBackend))
            return (user, None)


class IPBasedAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if settings.DEBUG:  # pragma: no cover
            ip = get_client_ip(request.META)
            if ip in conf.FREE_AUTH_IPS:
                User = get_user_model()
                user = User.objects.get_or_create(username=ip, email=f'noreply@{ip}.org')
                request.user = user
                # login(request, user, 'social_core.backends.azuread_tenant.AzureADTenantOAuth2')
                return (user, None)


class JWTAuthentication(authentication.JSONWebTokenAuthentication):
    def authenticate(self, request):

        jwt_value = self.get_jwt_value(request)

        if jwt_value is None:  # pragma: no cover
            return None

        try:
            user, jwt_value = super().authenticate(request)
            request.user = user
            # login(request, user, 'social_core.backends.azuread_tenant.AzureADTenantOAuth2')
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


def basicauth(view):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)

        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1].encode()).decode().split(':')
                    user = authenticate(username=uname, password=passwd)
                    if user is not None and user.is_active:
                        request.user = user
                        return view(request, *args, **kwargs)

        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="datamart"'
        return response

    return wrap
