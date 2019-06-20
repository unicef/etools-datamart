from functools import partial, partialmethod

from django.apps import apps

# from . import consts  # isort: skip noqa


def apply():
    # flake8: noqa: F401
    from . import (actionpoint, audit_engagement, auth_user, auth_usergroups, partners_intervention,
                   partners_partnerorganization, partners_plannedengagement, reports_appliedindicator,
                   tpm_activity, tpm_visit, partners_agreement, reports_lowerresult,
                   t2f_travel, t2f_travelactivity, users_userprofile, utils, )  # noqa
    from . import consts

    app_models = apps.get_app_config('etools').get_models()
    for model in app_models:
        for attr in ['name', 'username']:
            if hasattr(model, attr):
                setattr(model, '__str__', partialmethod(partial(utils.label, attr)))
                break

    from etools_datamart.apps.etools import models
    consts.enrich(models.ActionPointsActionpoint, consts.ActionPointConsts)
    consts.enrich(models.AuditEngagement, consts.AuditEngagementConsts)
