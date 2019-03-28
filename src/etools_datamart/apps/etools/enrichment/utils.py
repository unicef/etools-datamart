from django.db import models


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
