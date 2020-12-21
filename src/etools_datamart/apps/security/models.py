from django.contrib.auth.models import Group
from django.contrib.postgres.fields import ArrayField
from django.db import models


class SchemaAccessControl(models.Model):
    group = models.OneToOneField(Group, models.CASCADE, related_name='schemas')
    schemas = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    class Meta:
        verbose_name = 'Schemas ACL'
        verbose_name_plural = 'Schemas ACLs'
        ordering = ('group',)
