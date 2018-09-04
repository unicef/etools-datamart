# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission
from strategy_field.utils import fqn
from unicef_rest_framework.models import UserAccessControl


class URFPermission(BasePermission):
    serializer_field = "+serializer"

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        try:
            acl = UserAccessControl.objects.get(service__viewset=fqn(view))
            requested_serializer = request.GET.get(self.serializer_field, "std")

            return (acl.policy == UserAccessControl.POLICY_ALLOW and
                    (requested_serializer in acl.serializers) or ("*" in acl.serializers))
        except UserAccessControl.DoesNotExist:
            return True
