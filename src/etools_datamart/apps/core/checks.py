from unittest.mock import MagicMock

from django.core import checks
from django.core.checks import Error

from etools_datamart.api.urls import router


@checks.register()
def check_loader(app_configs, **kwargs):
    errors = []
    for prefix, viewset, basename in router.registry:
        if hasattr(viewset, 'querystringfilter_form_base_class'):
            view = viewset()
            form = view.get_querystringfilter_form(MagicMock(), MagicMock())
            a = set([a.split('__')[0] for a in form.fields.keys()])
            b = set(viewset.filter_fields)
            not_enabled = a - b
            if not_enabled:
                errors.append(Error('%s %s is present in form but not enabled' % (viewset.__name__, not_enabled)))
            # missed_in_form = b - a
            # if missed_in_form:
            #     errors.append(Error('%s form is missing %s' % (viewset.__name__, missed_in_form)))
    return errors
