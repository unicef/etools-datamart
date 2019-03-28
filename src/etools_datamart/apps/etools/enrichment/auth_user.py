
# Fix User ManyToManyField
from django.db import models

from etools_datamart.apps.etools.models import AuthGroup, AuthUserGroups, AuthUser
from unicef_security.models import User

models.ManyToManyField(AuthGroup,
                       through=AuthUserGroups,
                       ).contribute_to_class(AuthUser, 'groups')

AuthUser.is_authenticated = True
AuthUser.set_password = User.set_password

