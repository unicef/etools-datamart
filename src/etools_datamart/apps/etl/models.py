# -*- coding: utf-8 -*-

from django.db import models


class Execution(models.Model):
    task = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True)
    result = models.CharField(max_length=200)
    elapsed = models.IntegerField()
