import logging

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import ArrayField
from django.db import models

from .base import MasterDataModel
from .service import Service

logger = logging.getLogger(__name__)


class SerializerField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 200
        kwargs['name'] = 'serializer'
        super().__init__(*args, **kwargs)


def default_serializer():
    return ['std']


class AbstractAccessControl(MasterDataModel):
    POLICY_DENY = 0
    POLICY_ALLOW = 1
    POLICY_DEFAULT = 2  # not sure this is really needed.

    POLICIES = ((POLICY_DENY, "Forbid"),
                (POLICY_ALLOW, "Grant"),
                (POLICY_DEFAULT, "Default"),
                )
    service = models.ForeignKey(Service, models.CASCADE)
    rate = models.CharField(max_length=50, default="*")
    serializers = ArrayField(SerializerField(),
                             default=default_serializer,
                             blank=True)
    policy = models.IntegerField(choices=POLICIES, db_index=True)

    class Meta:
        abstract = True


class UserAccessControl(AbstractAccessControl):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='acl')

    class Meta:
        verbose_name = 'User ACL'
        verbose_name_plural = 'User ACLs'
        ordering = ('user', 'service')
        unique_together = ('user', 'service')

    def __str__(self):
        return f"{self.user}/{self.service}:{self.get_policy_display()}"


class GroupAccessControl(AbstractAccessControl):
    group = models.ForeignKey(Group, models.CASCADE, related_name='acl')

    class Meta:
        verbose_name = 'Group ACL'
        verbose_name_plural = 'Group ACLs'
        ordering = ('group', 'service')
        unique_together = ('group', 'service')

    def __str__(self):
        return f"{self.group}/{self.service}:{self.get_policy_display()}"
