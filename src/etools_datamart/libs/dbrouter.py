
def router_factory(db_name, app_list, syncdb=True):  # noqa

    class InnerRouter(object):

        def db_for_read(self, model, **hints):
            if model._meta.app_label in app_list:
                return db_name
            # elif get_model_name(model) in app_list:
            #     return db_name
            return None

        def db_for_write(self, model, **hints):
            if model._meta.app_label in app_list:
                return False
                # return db_name
            return None

        def allow_relation(self, obj1, obj2, **hints):
            if obj1._meta.app_label in app_list or obj2._meta.app_label in app_list:
                return True
            # elif get_model_name(obj1.__class__) in app_list or get_model_name(obj2.__class__) in app_list:
            #     return True
            return None

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            ret = None

            if db == db_name:
                ret = (app_label in app_list) and syncdb
            elif app_label in app_list:
                ret = False
            else:
                ret = None
            return ret

    return InnerRouter()
