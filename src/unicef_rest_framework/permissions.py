# -*- coding: utf-8 -*-
import logging

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from strategy_field.utils import fqn
from unicef_rest_framework.models import UserAccessControl
from unicef_rest_framework.models.acl import AbstractAccessControl, GroupAccessControl

logger = logging.getLogger(__name__)


class ServicePermission(BasePermission):
    serializer_field = "+serializer"

    def get_acl(self, request, view):
        try:
            return UserAccessControl.objects.get(service__viewset=fqn(view),
                                                 user=request.user)
        except GroupAccessControl.DoesNotExist:
            return GroupAccessControl.objects.get(service__viewset=fqn(view),
                                                  group__user=request.user)

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if not request.user.is_authenticated:
            return False
        try:
            acl = self.get_acl(request, view)

            if acl.policy == AbstractAccessControl.POLICY_DENY:
                logger.error(f"Access denied for user '{request.user}' to '{fqn(view)}'")
                raise PermissionDenied

            requested_serializer = request.GET.get(self.serializer_field, "std")

            if (requested_serializer not in acl.serializers) and ("*" not in acl.serializers):
                logger.error(
                    f"Forbidden serialiser '{requested_serializer}' for user '{request.user}' to '{fqn(view)}'")
                raise PermissionDenied(f"Forbidden serializer '{requested_serializer}'")

            return True
        except (UserAccessControl.DoesNotExist):
            logger.error(f"User '{request.user}' does not have grants for '{fqn(view)}'")
            return False
