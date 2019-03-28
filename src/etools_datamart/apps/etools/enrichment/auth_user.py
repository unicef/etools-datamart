
# Fix User ManyToManyField
from django.db import models

from unicef_security.models import User

from etools_datamart.apps.etools.models import AuthGroup, AuthUser, AuthUserGroups

models.ManyToManyField(AuthGroup,
                       through=AuthUserGroups,
                       ).contribute_to_class(AuthUser, 'groups')

AuthUser.is_authenticated = True
AuthUser.set_password = User.set_password
