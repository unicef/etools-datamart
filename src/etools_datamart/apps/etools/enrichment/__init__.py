from functools import partial, partialmethod

from django.apps import apps

from . import consts  # isort: skip


def apply():
    from . import (audit_engagement, auth_user, auth_usergroups, partners_intervention,
                   partners_partnerorganization, partners_plannedengagement, reports_appliedindicator,
                   t2f_travel, t2f_travelactivity, users_userprofile, utils, )

    app_models = apps.get_app_config('etools').get_models()
    for model in app_models:
        for attr in ['name', 'username']:
            if hasattr(model, attr):
                setattr(model, '__str__', partialmethod(partial(utils.label, attr)))
                break
