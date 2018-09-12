import importlib
import pkgutil

from django.core.checks import Error, register


def check_imports():
    import etools_datamart as package
    ""
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        current_module = '{}.{}'.format(package.__name__, modname)
        m = importlib.import_module(current_module)
        if hasattr(m, '__path__'):
            for _, sub_mod, __ in pkgutil.iter_modules(m.__path__):
                sub_module = '{}.{}'.format(current_module, sub_mod)
                sm = importlib.import_module(sub_module)
                if hasattr(sm, '__path__'):
                    for _, s_sub_mod, __ in pkgutil.iter_modules(sm.__path__):
                        s_sub_mod = '{}.{}.{}'.format(current_module, sub_mod, s_sub_mod)
                        try:
                            importlib.import_module(s_sub_mod)
                        except Exception as e:
                            raise Exception(f"""Error importing '{s_sub_mod}'.
    {e}
    """)


@register(deploy=True)
def check_importable(app_configs, **kwargs):
    errors = []
    try:
        check_imports()
    except Exception as e:
        errors.append(
            Error(
                str(e),
                hint='A hint.',
                obj=None,
                id='datamart.E001',
            )
        )
    return errors
