from functools import partial, partialmethod

from django.apps import apps

# from . import consts  # isort: skip noqa


def apply():
    # flake8: noqa: F401
    from . import (  # noqa
        actionpoint,
        audit_engagement,
        auth_user,
        consts,
        partners_agreement,
        partners_intervention,
        partners_partnerorganization,
        partners_plannedengagement,
        reports_appliedindicator,
        reports_lowerresult,
        t2f_travel,
        t2f_travelactivity,
        tpm_activity,
        tpm_partner,
        tpm_visit,
        users_userprofile,
        utils,
    )

    app_models = apps.get_app_config("etools").get_models()
    for model in app_models:
        for attr in ["name", "username"]:
            if hasattr(model, attr):
                setattr(model, "__str__", partialmethod(partial(utils.label, attr)))
                break

    from etools_datamart.apps.sources.etools import models

    consts.enrich(models.ActionPointsActionpoint, consts.ActionPointConsts)
    consts.enrich(models.AuditEngagement, consts.AuditEngagementConsts)
    consts.enrich(models.PartnersPartnerorganization, consts.PartnerOrganizationConst)
