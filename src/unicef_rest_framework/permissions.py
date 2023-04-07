import logging
from functools import lru_cache

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from strategy_field.utils import fqn

from unicef_rest_framework.acl import ACL_ACCESS_OPEN
from unicef_rest_framework.models import Service, UserAccessControl
from unicef_rest_framework.models.acl import AbstractAccessControl, GroupAccessControl

logger = logging.getLogger(__name__)


class ServicePermission(BasePermission):
    @lru_cache(10)
    def get_acl(self, request, service: Service):
        # PERF: this can be can be cached if we need to handle
        # consecutive OPTIONS/GET requests
        return list(UserAccessControl.objects.filter(service=service, user=request.user).order_by("-policy")) + list(
            GroupAccessControl.objects.filter(service=service, group__user=request.user).order_by("-policy")
        )

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if not request.user.is_authenticated:
            return False
        service = view.get_service()
        if service.access == ACL_ACCESS_OPEN:
            return True

        try:
            acls = self.get_acl(request, service)
            if not acls:
                return False
            requested_serializer = request.GET.get(view.serializer_field_param, "std")

            for acl in acls:
                if acl.policy == AbstractAccessControl.POLICY_DENY:
                    logger.error(f"Access denied for user '{request.user}' to '{fqn(view)}'")
                    raise PermissionDenied

                if (requested_serializer in acl.serializers) or ("*" in acl.serializers):
                    return True
                # if (requested_serializer not in acl.serializers) and ("*" not in acl.serializers):
                #     logger.error(
                #         f"Forbidden serializer '{requested_serializer}' for user '{request.user}' to '{fqn(view)}'")
                #     raise PermissionDenied(f"Forbidden serializer '{requested_serializer}'")
            raise PermissionDenied(f"Forbidden serializer '{requested_serializer}'")
            # return False
        except GroupAccessControl.DoesNotExist:
            logger.error(f"User '{request.user}' does not have grants for '{fqn(view)}'")
            return False
