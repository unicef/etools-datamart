from django.db import connections


def schemas(request):
    conn = connections["etools"]
    return {"schemas": conn.schemas}
