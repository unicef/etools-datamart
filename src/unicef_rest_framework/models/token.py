from django.conf import settings
from django.db import models

from .service import Service


class UserServiceToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    service = models.ForeignKey(Service, models.CASCADE)
    token = models.CharField(max_length=1000)
    expires = models.DateField(blank=True, null=True)
