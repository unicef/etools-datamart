from etools_datamart.apps.core.models import User
from etools_datamart.apps.sources.etools.models import AuthUser

AuthUser.is_authenticated = True
AuthUser.set_password = User.set_password


def get_display_name(self):
    if self.last_name and self.first_name:
        return "%s, %s" % (self.last_name, self.first_name)
    return self.username


AuthUser.get_display_name = get_display_name
