from rest_framework.versioning import URLPathVersioning


class URFVersioning(URLPathVersioning):
    allowed_versions = ['v1', 'v2']
