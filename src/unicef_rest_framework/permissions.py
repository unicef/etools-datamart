# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission
from strategy_field.utils import fqn
from unicef_rest_framework.models import UserAccessControl


class URFPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        try:
            acl = UserAccessControl.objects.get(service__viewset=fqn(view))
            return acl.policy == UserAccessControl.POLICY_ALLOW
        except UserAccessControl.DoesNotExist:
            return True
