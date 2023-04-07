import re
from importlib import import_module
from pathlib import Path

from django.contrib.admin import register
from django.contrib.admin.sites import AlreadyRegistered
from django.core.management.base import LabelCommand
from django.utils.module_loading import import_string

SER = """

class {realname}Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.{model}
        exclude = ()
"""

VIEWSET = """

class {realname}ViewSet(common.APIMultiTenantReadOnlyModelViewSet):
    serializer_class = serializers.{realname}Serializer
    queryset = models.{model}.objects.all()
"""

ADMIN = """

@register(models.{model})
class {model}Admin(TenantModelAdmin):
    pass

"""

SER_MODULE = """from etools_datamart.apps.etools import models
from rest_framework import serializers
"""

VIEWSET_MODULE = """from etools_datamart.apps.etools import models

from . import common
from .. import serializers
"""


class BuildException(Exception):
    pass


class Command(LabelCommand):
    help = "Process a Django Model and creates related ViewSet/Serializer "
    requires_system_checks = []
    args = "[modelname]"
    label = "model name"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--serializers",
            action="store",
            dest="serializers",
            default="etools_datamart.api.serializers",
            help="",
        )
        parser.add_argument(
            "--views",
            action="store",
            dest="views",
            default="etools_datamart.api.endpoints",
            help="",
        )
        parser.add_argument(
            "--urls",
            action="store",
            dest="urls",
            default="etools_datamart.api.urls",
            help="",
        )
        parser.add_argument(
            "--admin",
            action="store",
            dest="admin",
            default="etools_datamart.apps.etools.admin",
            help="",
        )

    def handle_label(self, modelname, **options):  # noqa
        try:
            try:
                model = import_string(f"etools_datamart.apps.etools.models.{modelname}")
            except ImportError:
                raise BuildException(f"Cannot find model {modelname} into 'etools_datamart.apps.etools.models' package")

            app, *name = re.findall("[A-Z][^A-Z]*", model.__name__)
            app_label = app.lower()
            realname = "".join(name)

            try:
                serializer_package = import_module(f"{options['serializers']}")
                serializer_module_path = Path(serializer_package.__file__).parent / f"{app_label}.py".lower()
            except ImportError:
                raise BuildException(f"Cannot import {options['serializers']}")

            try:
                view_package = import_module(f"{options['views']}")
                view_module_path = Path(view_package.__file__).parent / f"{app_label}.py".lower()
            except ImportError:
                raise BuildException(f"Cannot import {options['views']}")

            try:
                urls_module = import_module(f"{options['urls']}")
                urls_module_path = Path(urls_module.__file__)
            except ImportError:
                raise BuildException(f"Cannot import {options['urls']}")

            try:
                admin_module = import_module(f"{options['admin']}")
                admin_module_path = Path(admin_module.__file__)
            except ImportError:
                raise BuildException(f"Cannot import {options['admin']}")

        except BuildException as e:
            self.stderr.write(str(e))
            return

        # Serializer
        serializer_code = SER.format(model=modelname, realname=realname)

        if not serializer_module_path.exists():
            with open(str(serializer_module_path), "w") as f:
                f.write(SER_MODULE)

        try:
            import_string(f"{options['serializers']}.{app_label}.{realname}Serializer")
        except ImportError:
            with open(str(serializer_module_path), "a") as f:
                f.write(serializer_code)

        with open(serializer_package.__file__, "r") as f:
            content = f.read()
        with open(serializer_package.__file__, "w") as f:
            content = re.sub(f"from .{app_label} import \*  # noqa\n", "", content)
            content += f"from .{app_label} import *  # noqa\n"
            f.write(content)

        # ViewSet
        viewset_code = VIEWSET.format(model=modelname, realname=realname)

        if not view_module_path.exists():
            with open(str(view_module_path), "w") as f:
                f.write(VIEWSET_MODULE)

        try:
            import_string(f"{options['views']}.{app_label}.{realname}ViewSet")
        except ImportError:
            with open(str(view_module_path), "a") as f:
                f.write(viewset_code)

        with open(view_package.__file__, "r") as f:
            content = f.read()
        with open(view_package.__file__, "w") as f:
            content = re.sub(f"from .{app_label} import \*  # noqa\n", "", content)
            content += f"from .{app_label} import *  # noqa\n"
            f.write(content)

        # urls
        with open(urls_module_path, "r") as f:
            content = f.read()

        REGISTRATION = f"router.register(r'{app_label}/{realname.lower()}', views.{realname}ViewSet)"
        TARGET = "urlpatterns = router.urls"

        with open(urls_module_path, "w") as f:
            content = re.sub(f"\n{TARGET}\n", f"{REGISTRATION}\n\n{TARGET}\n", content)
            f.write(content)

        # admin
        admin_code = ADMIN.format(model=modelname, realname=realname)

        try:
            register(model)
        except AlreadyRegistered:
            pass
        else:
            with open(admin_module_path, "a") as f:
                f.write(admin_code)
