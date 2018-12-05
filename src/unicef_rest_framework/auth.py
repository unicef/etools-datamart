import logging

from constance import config
from crashlog.middleware import process_exception
from django.contrib.auth import get_user_model, login
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework_jwt import authentication
from unicef_security.graph import default_group, Synchronizer

logger = logging.getLogger()


def jwt_get_username_from_payload(payload):
    return payload.get('preferred_username', payload.get('unique_name'))


class JWTAuthentication(authentication.JSONWebTokenAuthentication):
    def authenticate(self, request):

        jwt_value = self.get_jwt_value(request)

        if jwt_value is None:  # pragma: no cover
            return None

        try:
            user, jwt_value = super(JWTAuthentication, self).authenticate(request)
            request.user = user
            login(request, user, 'social_core.backends.azuread_tenant.AzureADTenantOAuth2')
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


# AQABAAIAAAC5una0EUFgTIF8ElaxtWjTE8f9OcsbHLLnobNloaTfC--E_fRoUrtiw2jul5yBV9rN3CO2C1BJ2IB99esAhsuRrzEowH3COPLFe5hkhovi4zfceFjwu6iSXpfgAFVGuo_fmep0osVwr0WkFzhWI5QEgNNnrf7d7gFm4iVC4gFE24R_JymglPADBvJIUMGAPHYg-IEyK1GKSkzpNSjJNZz6Pad_uVlDMrssFcrRqxKOJzqIhggLq7XQpJnmfUF5dJNdriDMkUjHBhDqlNpKTJZpnJg0jfIn7843kmKH0WXbJL0ss-tfgc_d8Q0240bdYXX6YSBV20NPx7MHy5V9i1RAtmr11cHBCw3uDuRriomgOhtIxTKYLox8iKYHbELA9Opvd-zLJm9krxoxlEHVO-PKl11No1mT8ZC83Ox37yxG5vrE7U7UxaLml9PmrjRZQoD1HvJ354IxZyP2pytYq2XhvIG_NDSDfuO5hwzPKb9F7G4Hytu96plKlu_yvdZ4Gghbp7z2sryeAiCnpYNlskGVUrQwF7BSHT73XuuOWeFelp-jn3tR4LQwqEGkg3zLqswcjbsRykSvS3cY6xTdBsCb7H70nygnhOgr_WlT9oY9KS2ElBVU-Q8OE8mkJ1rDV42hRb-haC7yzyUgtofbSQdVMIUgJRpuxYCrHNJ5oRsXmrWI0EVTdWFN25kwOMYPwOI8rzVf1oHikTQiHm3AN5wz0ill40IfjLB9niMEn4kntLDGJU1rIeALxv1s4lHxMZHpc1YEgLTf_3LnGtrsca3bIAA
