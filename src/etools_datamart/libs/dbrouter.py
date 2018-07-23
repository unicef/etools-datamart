def router_factory(db_name, app_list, syncdb=True):  # noqa
    def get_model_name(model):
        return (".".join([model._meta.app_label, model.__name__])).lower()

    class InnerRouter(object):
        """ A router to control all database operations on models in
        the myapp application """

        def db_for_read(self, model, **hints):
            """ Point all operations on myapp models to 'other' """
            if model._meta.app_label in app_list:
                return db_name
            elif get_model_name(model) in app_list:
                return db_name
            return None

        def db_for_write(self, model, **hints):
            """ Point all operations on myapp models to 'other' """
            if hasattr(model, "_meta") and model._meta.app_label in app_list:
                return db_name
            return None

        def allow_relation(self, obj1, obj2, **hints):
            """ Allow any relation if a model in myapp is involved """
            if obj1._meta.app_label in app_list or obj2._meta.app_label in app_list:
                return True
            elif get_model_name(obj1.__class__) in app_list or get_model_name(obj2.__class__) in app_list:
                return True
            return None

        def allow_migrate(self, db, model):
            return self.allow_syncdb(db, model)

        def allow_syncdb(self, db, model):
            """ Make sure the myapp app only appears on the 'other' db """
            ret = None

            if db == db_name:
                ret = (model._meta.app_label in app_list) and syncdb
            elif model._meta.app_label in app_list:
                ret = False
            elif get_model_name(model) in app_list:
                return False
            else:
                ret = None
            return ret

    return InnerRouter()
