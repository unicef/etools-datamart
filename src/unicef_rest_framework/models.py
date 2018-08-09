# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import Group, Permission, User
from django.db import models


class Team(models.Model):
    users = models.ManyToManyField(User)


class Role(models.Model):
    permissions = models.ManyToManyField(Permission)


class Authorization(models.Model):
    team = models.ForeignKey(Team, models.CASCADE)
    role = models.ForeignKey(Role, models.CASCADE)

