from contextlib import ContextDecorator

from test_utilities.factories import BusinessAreaFactory, RoleFactory
from unicef_rest_framework.models import Service, UserAccessControl
from unicef_security.models import Role


class user_allow_country(ContextDecorator):  # noqa
    def __init__(self, user, coutries=None):
        self.user = user
        if not isinstance(coutries, (list, tuple)):
            coutries = [coutries]
        self.areas = [BusinessAreaFactory(name=s) for s in coutries]
        self.rules = []

    def __enter__(self):
        for area in self.areas:
            rule = RoleFactory(user=self.user, business_area=area)
            self.rules.append(rule.pk)

    def __exit__(self, e_typ, e_val, trcbak):
        Role.objects.filter(id__in=self.rules).delete()
        if e_typ:
            raise e_typ(e_val).with_traceback(trcbak)

    def start(self):
        """Activate a patch, returning any created mock."""
        result = self.__enter__()
        return result

    def stop(self):
        """Stop an active patch."""
        return self.__exit__(None, None, None)


class user_allow_service(ContextDecorator):  # noqa
    def __init__(self, user, viewsets=None):
        self.user = user
        if not isinstance(viewsets, (list, tuple)):
            viewsets = [viewsets]
        self.services = [s for s in [Service.objects.get(viewset=v) for v in viewsets]]
        self.rules = []

    def __enter__(self):
        for service in self.services:
            rule = UserAccessControl.objects.get_or_create(user=self.user,
                                                           service=service,
                                                           policy=UserAccessControl.POLICY_ALLOW
                                                           )[0]
            self.rules.append(rule.pk)

    def __exit__(self, e_typ, e_val, trcbak):
        UserAccessControl.objects.filter(id__in=self.rules).delete()
        if e_typ:
            raise e_typ(e_val).with_traceback(trcbak)

    def start(self):
        """Activate a patch, returning any created mock."""
        result = self.__enter__()
        return result

    def stop(self):
        """Stop an active patch."""
        return self.__exit__(None, None, None)
