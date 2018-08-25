# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from strategy_field.utils import import_by_name

from .cache import parse_ttl
from .models import CacheVersion, Service


class CacheVersionForm(ModelForm):
    class Meta:
        model = CacheVersion
        fields = ('name', 'cache_version', 'cache_ttl', 'cache_key')

    def clean_cache_ttl(self):
        value = self.cleaned_data['cache_ttl']
        try:
            parse_ttl(value)
        except Exception:
            raise ValidationError('Invalid TTL')
        return value


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

    def clean_viewset(self):
        value = self.cleaned_data['viewset']
        try:
            import_by_name(value)
        except Exception:
            raise ValidationError(value)
        return value
