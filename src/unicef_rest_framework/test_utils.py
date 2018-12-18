from contextlib import ContextDecorator

from test_utilities.factories import GroupFactory
from unicef_rest_framework.models import Service, UserAccessControl

from etools_datamart.apps.security.models import SchemaAccessControl


class user_allow_country(ContextDecorator):  # noqa
    def __init__(self, user, countries=None):
        self.user = user
        if not isinstance(countries, (list, tuple, set)):
            countries = [countries]
        self.areas = countries
        self.rule = None

    def __enter__(self):
        self.group = GroupFactory()
        self.group.user_set.add(self.user)
        self.rule = SchemaAccessControl.objects.get_or_create(group=self.group,
                                                              schemas=self.areas)[0]

    def __exit__(self, e_typ, e_val, trcbak):
        self.group.delete()
        self.rule.delete()
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
