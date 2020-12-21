import logging

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from .base import MasterDataModel
from .service import Service

logger = logging.getLogger(__name__)


class Application(MasterDataModel):
    name = models.CharField(_('Name'), max_length=100, unique=True, db_index=True)
    description = models.TextField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
    allowed_ip = models.CharField(max_length=255, default='.*', help_text='Regex to validate remote IP')
    all_services = models.BooleanField(default=False, help_text='allow any service, even future created')
    services = models.ManyToManyField(Service,
                                      blank=True,
                                      help_text='allowed services')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)
    #
    # def check_password(self, raw_password):
    #     """
    #     Returns a boolean of whether the raw_password was correct. Handles
    #     hashing formats behind the scenes.
    #     """
    #
    #     def setter(raw_password):
    #         self.set_password(raw_password)
    #         self.save(update_fields=["password"])
    #
    #     return check_password(raw_password, self.password, setter)
    #
    # def has_perm(self, perm):
    #     return False
