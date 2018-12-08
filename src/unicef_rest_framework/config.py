# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.urls import get_callable
from strategy_field.utils import import_by_name
from unicef_rest_framework import acl


class AppSettings(object):
    defaults = {
        'API_CACHE': 'default',
        'FREE_AUTH_IPS': [],
        'ROUTER': 'unicef_rest_framework.urls.router',
        'DEFAULT_ACCESS': acl.ACL_ACCESS_LOGIN,
        'get_current_user': 'get_current_user',
        'get_current_request': 'get_current_request',
    }

    def __init__(self, prefix):
        """
        Loads our settings from django.conf.settings, applying defaults for any
        that are omitted.
        """
        self.prefix = prefix
        setting_changed.connect(self._handler)

    def __getattr__(self, name):
        if name in self.defaults.keys():
            from django.conf import settings
            name_with_prefix = (self.prefix + '_' + name).upper()
            raw_value = getattr(settings, name_with_prefix, self.defaults[name])
            value = self._set_attr(name_with_prefix, raw_value)
            setattr(settings, name_with_prefix, raw_value)
            setting_changed.send(self.__class__, setting=name_with_prefix, value=raw_value, enter=True)
            return value
        raise AttributeError(name)

    def _set_attr(self, prefix_name, value):
        name = prefix_name[len(self.prefix) + 1:]
        if name in ('ROUTER', ):
            try:
                obj = import_by_name(value)
            except (ImportError, ValueError, AttributeError):
                raise ImportError(f"Cannot import '{value}'. Check your settings.{prefix_name}")
            setattr(self, name, obj)
            return obj
        elif name in ('get_current_user', 'get_current_request', 'get_current_user'):
            try:
                if isinstance(value, str):
                    func = get_callable(value)
                elif callable(value):
                    func = value
                else:
                    raise ImproperlyConfigured(
                        f"{value} is not a valid value for `{name}`. "
                        "It must be a callable or a fullpath to callable. ")
            except Exception as e:
                raise ImproperlyConfigured(e)
            setattr(self, name, func)
            return func
        else:
            setattr(self, name, value)
            return value

    def _handler(self, sender, setting, value, **kwargs):
        """
            handler for ``setting_changed`` signal.

        @see :ref:`django:setting-changed`_
        """
        if setting.startswith(self.prefix):
            name = setting[len(self.prefix) + 1:]
            try:
                delattr(self, name)
            except AttributeError:
                pass


conf = AppSettings('UNICEF_REST_FRAMEWORK')
