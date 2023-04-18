import json

from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput
from django.forms.models import ModelForm

from strategy_field.utils import import_by_name

from unicef_rest_framework.models import Export

from .cache import parse_ttl
from .models import CacheVersion, Service


class CacheVersionForm(ModelForm):
    class Meta:
        model = CacheVersion
        fields = ("name", "cache_version", "cache_ttl", "cache_key")

    def clean_cache_ttl(self):
        value = self.cleaned_data["cache_ttl"]
        try:
            parse_ttl(value)
        except Exception:
            raise ValidationError("Invalid TTL")
        return value


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

    def clean_viewset(self):
        value = self.cleaned_data["viewset"]
        try:
            import_by_name(value)
        except Exception:
            raise ValidationError(value)
        return value


class Select2ChoiceField(forms.ChoiceField):
    def widget_attrs(self, widget):
        return {"class": "select2"}


class CleareableSelect2ChoiceField(forms.ChoiceField):
    def widget_attrs(self, widget):
        return {"class": "select2", "data-allowclear": "true"}


class Select2MultipleChoiceField(forms.MultipleChoiceField):
    def widget_attrs(self, widget):
        return {"class": "select2"}


class CleareableSelect2MultipleChoiceField(forms.MultipleChoiceField):
    def widget_attrs(self, widget):
        return {"class": "select2", "data-allowclear": "true"}


class DatePickerField(forms.DateField):
    def widget_attrs(self, widget):
        return {
            "class": "datepicker",
            "autocomplete": "off",
            "data-pickeroptions": json.dumps(
                {"format": "yyyy-mm-dd", "orientation": "bottom", "autoclose": True, "clearBtn": True}
            ),
        }


class DateRangePickerWidget(forms.MultiWidget):
    template_name = "widgets/daterange.html"

    def __init__(self, till_today=True, attrs=None):
        widgets = (
            DateInput(),
            DateInput(),
        )
        super().__init__(widgets, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        return [
            self.widgets[0].value_from_datadict(data, files, name + "__gte"),
            self.widgets[1].value_from_datadict(data, files, name + "__lte"),
        ]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if not isinstance(value, list):
            value = self.decompress(value)
        subwidgets = []
        final_attrs = context["widget"]["attrs"]

        id_ = final_attrs.get("id")
        for i, op in enumerate(["gte", "lte"]):
            widget = self.widgets[i]
            widget_attrs = final_attrs.copy()
            widget_attrs.update(self.widget_attrs(widget))
            widget_attrs["id"] = "%s_%s" % (id_, op)

            w = widget.get_context("%s__%s" % (name, op), value[i], widget_attrs)
            if i == 1:
                w["widget"]["attrs"]["class"] += " end-range"
                w["widget"]["attrs"]["data-start-range"] = "#" + "%s_gte" % id_
            else:
                w["widget"]["attrs"]["class"] += " start-range"
                w["widget"]["attrs"]["data-end-range"] = "#" + "%s_lte" % id_

            subwidgets.append(w["widget"])
        context["widget"]["subwidgets"] = subwidgets
        return context

    def widget_attrs(self, widget):
        defaults = {
            "class": "datepicker form-control",
            "autocomplete": "off",
        }
        picker = {"format": "yyyy-mm-dd", "orientation": "auto", "autoclose": True, "clearBtn": True}
        defaults["data-pickeroptions"] = json.dumps(picker)
        return defaults


class DateRangePickerField(forms.MultiValueField):
    widget = DateRangePickerWidget

    def __init__(self, input_formats=None, **kwargs):
        localize = kwargs.get("localize", False)
        fields = (
            DatePickerField(input_formats=input_formats, localize=localize, **kwargs),
            DatePickerField(input_formats=input_formats, localize=localize, **kwargs),
        )
        super().__init__(fields, **kwargs)

    def widget_attrs(self, widget):
        return {"class": "form-control"}

    def compress(self, data_list):
        if not data_list or (not data_list[0] and not data_list[1]):
            return None, None
        if data_list[0] and data_list[1]:
            if data_list[0] > data_list[1]:
                raise ValidationError("Start Date cannot be greater than than End Date")
        return data_list


class ExportForm(forms.ModelForm):
    class Meta:
        model = Export
        fields = ("id", "name", "format", "refresh", "filename", "save_as", "enabled")

    def __init__(self, instance=None, url=None, params=None, **kwargs):
        if instance is None:
            self.url = url
            self.params = params
        else:
            self.url = instance.url
            self.params = instance.params
        super().__init__(instance=instance, **kwargs)

    def save(self, commit=True):
        self.instance.url = self.url
        self.instance.params = self.params
        return super().save(commit)
