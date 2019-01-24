from django.apps import apps
from django.core import checks
from django.core.checks import Error

from etools_datamart.apps.data.loader import loadeables


@checks.register()
def check_loader(app_configs, **kwargs):
    errors = []
    for model_name in loadeables:
        model = apps.get_model(model_name)
        cfg = model.loader.config
        # if cfg.queryset  is None and  cfg.source is None:
        #     errors.append(Error(
        #         "LoaderOptions must set 'source' or 'queryset' attribunte",
        #         hint='',
        #         obj=model.loader,
        #         id='H001',
        #     ))
        if cfg.last_modify_field:
            try:
                cfg.source._meta.get_field(cfg.last_modify_field)
            except Exception:
                errors.append(Error(
                    f"LoaderOptions last_modify_field: '{cfg.last_modify_field}' does not exists in {cfg.source}",
                    hint='',
                    obj=model.loader,
                    id='L001',
                ))

    return errors
