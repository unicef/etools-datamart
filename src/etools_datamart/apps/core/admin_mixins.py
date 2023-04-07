from django.db import models

from admin_extra_buttons.mixins import ExtraButtonsMixin


class ReadOnlyMixin:
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DisplayAllMixin:
    def get_list_display(self, request):  # pragma: no cover
        if self.list_display == ("__str__",):
            return [
                field.name
                for field in self.model._meta.fields
                if not (
                    isinstance(field, models.ForeignKey)
                    or field.name
                    in [
                        "seen",
                        "created",
                        "uuid",
                        "country_name",
                        "area_code",
                        "source_id",
                        "modified",
                        "last_modify_date",
                    ]
                )
            ]
        return self.list_display


class DatamartSourceModelAdmin(ReadOnlyMixin, ExtraButtonsMixin, DisplayAllMixin):
    pass


class DatamartModelAdmin(ExtraButtonsMixin, DisplayAllMixin):
    pass
