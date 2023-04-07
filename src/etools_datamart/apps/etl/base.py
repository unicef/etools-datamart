from django.db.models.base import ModelBase


class DataMartModelBase(ModelBase):
    loader_option_class = None
    loader_class = None

    def __new__(cls, name, bases, attrs, **kwargs):
        super_new = super().__new__
        parents = [b for b in bases if isinstance(b, DataMartModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)
        loader = attrs.pop("loader", None)
        config = attrs.pop("Options", None)

        new_class = super_new(cls, name, bases, attrs, **kwargs)
        if not loader:  # no custom loader use default
            loader = cls.loader_class()
        base_config = getattr(new_class, "_etl_config", None)

        if not config:
            config = cls.loader_option_class(base_config)
        else:
            config = cls.loader_option_class(config)

        new_class.add_to_class("_etl_config", config)
        new_class.add_to_class("loader", loader)
        #
        # attr_meta = attrs.get('Meta', None)
        # attr_loader = attrs.get('Loader', None)
        # loader = attr_meta or getattr(new_class, 'Meta', None)
        # base_meta = getattr(new_class, '_meta', None)

        return new_class
