from django.db import models
from django.db.models import AutoField
from django.utils.datastructures import ImmutableList


def label(attr, self):
    return getattr(self, attr)


def create_alias(model, aliases):
    for related, business_name in aliases:
        r = getattr(model, related)
        setattr(model, business_name, r)


def add_m2m(master, name: str, detail, through):
    models.ManyToManyField(detail,
                           through=through,
                           ).contribute_to_class(master, name)


def add_m2m2(master, name: str, detail, through):
    models.ManyToManyField(detail,
                           through=through,
                           ).contribute_to_class(master, name)


def set_primary_key(model, field_name):
    pk = model._meta.get_field(field_name)
    model._meta.pk = pk
    model._meta.auto_field = pk
    model._meta.fields = ImmutableList([f for f in model._meta.fields
                                        if not isinstance(f, AutoField)])
