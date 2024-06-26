import logging
import uuid

from django import forms
from django.contrib import admin

from admin_extra_buttons.mixins import ExtraButtonsMixin

from unicef_rest_framework.models import Application

logger = logging.getLogger(__name__)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = "__all__"

    def clean_password(self):
        if "password" not in self.cleaned_data or self.cleaned_data["password"] == "":
            return uuid.uuid4()
        else:
            return self.cleaned_data["password"]


class ApplicationAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    readonly_fields = ("uuid", "last_modify_user")
    form = ApplicationForm
    exclude = ("all_services",)
    search_fields = ("name", "uuid")
    list_display = ("name", "user")
    filter_horizontal = ("services",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(*self.raw_id_fields)
