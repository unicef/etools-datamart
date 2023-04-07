def router_factory(db_name, app_list, syncdb=True):  # noqa
    class InnerRouter(object):
        def db_for_read(self, model, **hints):
            if model._meta.app_label in app_list:
                return db_name
            return None

        def db_for_write(self, model, **hints):
            if model._meta.app_label in app_list:  # pragma: no cover
                return db_name
            return None

        def allow_relation(self, obj1, obj2, **hints):
            if obj1._meta.app_label in app_list or obj2._meta.app_label in app_list:
                return True
            # No opinion if neither object is in the Example app (defer to default or other routers).
            elif db_name not in [obj1._meta.app_label, obj2._meta.app_label]:
                return None
            # Block relationship if one object is in the Example app and the other isn't.
            return False

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            """Ensure that the Example app's models get created on the right database."""
            # if syncdb and app_label in app_list:
            #     # The Example app should be migrated only on the example_db database.
            #     return db == db_name
            # elif syncdb and (db == db_name):
            #     # Ensure that all other apps don't get migrated on the example_db database.
            #     return False
            #
            # # No opinion for all other scenarios
            # return None
            # ret = None

            if db == db_name:  # pragma: no cover
                ret = (app_label in app_list) and syncdb
            elif app_label in app_list:
                ret = False
            else:
                ret = None
            return ret

    return InnerRouter()
